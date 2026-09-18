from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal
from .models import Patient, Policy, Coverage
from backend.verification import (
    verify_insurance,
    calculate_cost_estimate,
    verify_multiple_procedures
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "DentalVerify API is running!"
    }


# ==========================================
# INSURANCE VERIFICATION
# ==========================================

@app.get("/patient/{member_id}")
def get_patient(
    member_id: str,
    procedure_code: str,
    procedure_cost: float
):

    db = SessionLocal()


    # Find patient
    patient = db.query(Patient).filter(
        Patient.member_id == member_id
    ).first()

    if patient is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    # Find policy
    policy = db.query(Policy).filter(
        Policy.member_id == member_id
    ).first()

    if policy is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Insurance policy not found"
        )


    # Find the requested procedure
    coverage = db.query(Coverage).filter(
        Coverage.member_id == member_id,
        Coverage.procedure_code == procedure_code
    ).first()

    if coverage is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Procedure not found for this patient"
        )


    # Run insurance verification
    verification_result = verify_insurance(
        policy,
        coverage
    )


    # Calculate estimated cost
    cost_estimate = calculate_cost_estimate(
        procedure_cost,
        coverage.coverage_percentage,
        policy.deductible_remaining,
        policy.remaining_limit
    )


    db.close()


    return {

        "patient": {
            "name": patient.name,
            "dob": patient.dob,
            "member_id": patient.member_id,
            "provider": patient.provider
        },


        "policy": {
            "status": policy.status,
            "start_date": policy.start_date,
            "end_date": policy.end_date,
            "annual_limit": policy.annual_limit,
            "remaining_limit": policy.remaining_limit,
            "deductible": policy.deductible,
            "deductible_remaining": policy.deductible_remaining
        },


        "coverage": {
            "procedure_code": coverage.procedure_code,
            "procedure_name": coverage.procedure_name,
            "coverage_percentage": coverage.coverage_percentage,
            "frequency_limit": coverage.frequency_limit,
            "times_used": coverage.times_used
        },


        "verification": verification_result,


        "cost_estimate": cost_estimate

    }


# ==========================================
# PATIENT INFORMATION LOOKUP
# ==========================================

@app.get("/patient/{member_id}/info")
def get_patient_info(member_id: str):

    db = SessionLocal()


    # Find patient
    patient = db.query(Patient).filter(
        Patient.member_id == member_id
    ).first()

    if patient is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    # Find insurance policy
    policy = db.query(Policy).filter(
        Policy.member_id == member_id
    ).first()

    if policy is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Insurance policy not found"
        )


    db.close()


    return {

        "name": patient.name,
        "dob": patient.dob,
        "member_id": patient.member_id,
        "provider": patient.provider,
        "policy_status": policy.status

    }


# ==========================================
# DENTAL PROCEDURE LOOKUP
# ==========================================

@app.get("/patient/{member_id}/procedures")
def get_patient_procedures(member_id: str):

    db = SessionLocal()


    # Check if patient exists
    patient = db.query(Patient).filter(
        Patient.member_id == member_id
    ).first()

    if patient is None:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    # Find all dental procedures for this patient
    coverages = db.query(Coverage).filter(
        Coverage.member_id == member_id
    ).all()

    db.close()


    if not coverages:
        raise HTTPException(
            status_code=404,
            detail="No dental procedures found"
        )


    return {

        "member_id": member_id,

        "provider": patient.provider,

        "procedures": [

            {
                "procedure_code": coverage.procedure_code,
                "procedure_name": coverage.procedure_name,
                "coverage_percentage": coverage.coverage_percentage,
                "frequency_limit": coverage.frequency_limit,
                "times_used": coverage.times_used
            }

            for coverage in coverages

        ]

    }


# ==========================================
# MULTIPLE PROCEDURE VERIFICATION
# ==========================================

@app.post("/patient/{member_id}/verify-multiple")
def verify_multiple(
    member_id: str,
    data: dict
):

    db = SessionLocal()


    # ------------------------------------------
    # FIND PATIENT
    # ------------------------------------------

    patient = db.query(Patient).filter(
        Patient.member_id == member_id
    ).first()

    if patient is None:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    # ------------------------------------------
    # FIND POLICY
    # ------------------------------------------

    policy = db.query(Policy).filter(
        Policy.member_id == member_id
    ).first()

    if policy is None:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Insurance policy not found"
        )


    # ------------------------------------------
    # GET PROCEDURES FROM REQUEST
    # ------------------------------------------

    procedures = data.get("procedures")

    if not procedures:

        db.close()

        raise HTTPException(
            status_code=400,
            detail="No procedures provided"
        )


    # ------------------------------------------
    # FIND COVERAGE FOR EACH PROCEDURE
    # ------------------------------------------

    coverages = []

    procedure_costs = {}


    for procedure in procedures:

        procedure_code = procedure.get(
            "procedure_code"
        )

        procedure_cost = procedure.get(
            "procedure_cost"
        )


        if not procedure_code:

            db.close()

            raise HTTPException(
                status_code=400,
                detail="Procedure code is required"
            )


        if procedure_cost is None:

            db.close()

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Procedure cost is required "
                    f"for {procedure_code}"
                )
            )


        # Find procedure coverage
        coverage = db.query(Coverage).filter(
            Coverage.member_id == member_id,
            Coverage.procedure_code == procedure_code
        ).first()


        if coverage is None:

            db.close()

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Procedure {procedure_code} "
                    "not found for this patient"
                )
            )


        coverages.append(coverage)

        procedure_costs[procedure_code] = float(
            procedure_cost
        )


    # ------------------------------------------
    # VERIFY ALL PROCEDURES
    # ------------------------------------------

    verification_result = verify_multiple_procedures(
        policy,
        coverages,
        procedure_costs
    )


    db.close()


    # ------------------------------------------
    # RETURN RESULT
    # ------------------------------------------

    return {

        "patient": {

            "name": patient.name,

            "dob": patient.dob,

            "member_id": patient.member_id,

            "provider": patient.provider

        },


        "policy": {

            "status": policy.status,

            "start_date": policy.start_date,

            "end_date": policy.end_date,

            "annual_limit": policy.annual_limit,

            "remaining_limit": policy.remaining_limit,

            "deductible": policy.deductible,

            "deductible_remaining":
                policy.deductible_remaining

        },


        "verification": verification_result

    }