def verify_insurance(policy, coverage):
    results = []

    # 1. Check insurance status
    if policy.status == "Active":
        results.append({
            "check": "Insurance Status",
            "status": "PASS",
            "message": "Insurance is active."
        })

    elif policy.status in ["Expired", "Cancelled"]:
        results.append({
            "check": "Insurance Status",
            "status": "FAIL",
            "message": f"Insurance status is {policy.status}."
        })

    else:
        results.append({
            "check": "Insurance Status",
            "status": "INFO",
            "message": (
                f"Insurance status is {policy.status}. "
                "Manual review required."
            )
        })

    # 2. Check procedure coverage
    if coverage.coverage_percentage > 0:
        results.append({
            "check": "Procedure Coverage",
            "status": "PASS",
            "message": (
                f"{coverage.procedure_name} is covered at "
                f"{coverage.coverage_percentage:.0f}%."
            )
        })

    else:
        results.append({
            "check": "Procedure Coverage",
            "status": "FAIL",
            "message": (
                f"{coverage.procedure_name} is not covered."
            )
        })

    # 3. Check frequency limit
    if coverage.times_used < coverage.frequency_limit:
        results.append({
            "check": "Frequency Limit",
            "status": "PASS",
            "message": (
                f"{coverage.frequency_limit - coverage.times_used} "
                "usage(s) remaining."
            )
        })

    else:
        results.append({
            "check": "Frequency Limit",
            "status": "FAIL",
            "message": "Frequency limit has been reached."
        })

    # 4. Check annual maximum
    if policy.remaining_limit > 0:
        results.append({
            "check": "Annual Maximum",
            "status": "PASS",
            "message": (
                f"${policy.remaining_limit:.2f} "
                "remaining for the year."
            )
        })

    else:
        results.append({
            "check": "Annual Maximum",
            "status": "FAIL",
            "message": (
                "Annual insurance maximum has been reached."
            )
        })

    # 5. Check deductible
    if policy.deductible_remaining > 0:
        results.append({
            "check": "Deductible",
            "status": "INFO",
            "message": (
                f"${policy.deductible_remaining:.2f} "
                "remaining on the deductible."
            )
        })

    else:
        results.append({
            "check": "Deductible",
            "status": "PASS",
            "message": "Deductible has been met."
        })

    # Determine overall status
    failed_checks = [
        result
        for result in results
        if result["status"] == "FAIL"
    ]

    info_checks = [
        result
        for result in results
        if result["status"] == "INFO"
    ]

    if len(failed_checks) > 0:
        overall_status = "NOT ELIGIBLE"

    elif len(info_checks) > 0:
        overall_status = "NEEDS REVIEW"

    else:
        overall_status = "ELIGIBLE"

    return {
        "overall_status": overall_status,
        "checks": results
    }


# ==========================================
# COST ESTIMATION
# ==========================================

def calculate_cost_estimate(
    procedure_cost,
    coverage_percentage,
    deductible_remaining,
    remaining_annual_limit
):
    """
    Calculate an estimated insurance payment
    and patient responsibility.

    This is a prototype estimate and does not
    represent real insurance claim adjudication.
    """

    # Apply deductible first
    deductible_applied = min(
        procedure_cost,
        deductible_remaining
    )

    # Amount remaining after deductible
    amount_after_deductible = (
        procedure_cost - deductible_applied
    )

    # Calculate insurance payment
    insurance_pays = (
        amount_after_deductible
        * (coverage_percentage / 100)
    )

    # Insurance cannot exceed remaining annual maximum
    insurance_pays = min(
        insurance_pays,
        remaining_annual_limit
    )

    # Patient pays the remaining amount
    patient_responsibility = (
        procedure_cost - insurance_pays
    )

    return {
        "procedure_cost": round(
            procedure_cost,
            2
        ),

        "deductible_applied": round(
            deductible_applied,
            2
        ),

        "amount_after_deductible": round(
            amount_after_deductible,
            2
        ),

        "coverage_percentage": coverage_percentage,

        "estimated_insurance_payment": round(
            insurance_pays,
            2
        ),

        "estimated_patient_responsibility": round(
            patient_responsibility,
            2
        )
    }


# ==========================================
# MULTIPLE PROCEDURE VERIFICATION
# ==========================================

def verify_multiple_procedures(
    policy,
    coverages,
    procedure_costs
):
    """
    Verify multiple dental procedures for the same
    patient and calculate a combined cost estimate.

    The deductible and annual maximum are applied
    across the entire group of procedures.
    """

    procedure_results = []

    total_cost = 0
    total_insurance_payment = 0
    total_patient_responsibility = 0

    # Track remaining deductible and annual maximum
    remaining_deductible = policy.deductible_remaining
    remaining_annual_limit = policy.remaining_limit

    for coverage in coverages:

        procedure_code = coverage.procedure_code

        procedure_cost = procedure_costs.get(
            procedure_code,
            0
        )

        # ------------------------------------------
        # COVERAGE CHECK
        # ------------------------------------------

        if coverage.coverage_percentage > 0:

            coverage_status = "PASS"

            coverage_message = (
                f"{coverage.procedure_name} is covered at "
                f"{coverage.coverage_percentage:.0f}%."
            )

        else:

            coverage_status = "FAIL"

            coverage_message = (
                f"{coverage.procedure_name} is not covered."
            )

        # ------------------------------------------
        # FREQUENCY CHECK
        # ------------------------------------------

        if coverage.times_used < coverage.frequency_limit:

            frequency_status = "PASS"

            frequency_message = (
                f"{coverage.frequency_limit - coverage.times_used} "
                "usage(s) remaining."
            )

        else:

            frequency_status = "FAIL"

            frequency_message = (
                "Frequency limit has been reached."
            )

        # ------------------------------------------
        # COST CALCULATION
        # ------------------------------------------

        # If procedure is not covered or frequency
        # limit has been reached, insurance pays $0.

        if (
            coverage_status == "FAIL"
            or
            frequency_status == "FAIL"
        ):

            deductible_applied = 0

            amount_after_deductible = procedure_cost

            insurance_payment = 0

        else:

            # Apply remaining deductible
            deductible_applied = min(
                procedure_cost,
                remaining_deductible
            )

            amount_after_deductible = (
                procedure_cost
                - deductible_applied
            )

            # Reduce remaining deductible
            remaining_deductible -= deductible_applied

            # Calculate insurance payment
            insurance_payment = (
                amount_after_deductible
                * (
                    coverage.coverage_percentage
                    / 100
                )
            )

            # Apply remaining annual maximum
            insurance_payment = min(
                insurance_payment,
                remaining_annual_limit
            )

            # Reduce remaining annual maximum
            remaining_annual_limit -= insurance_payment

        # ------------------------------------------
        # PATIENT RESPONSIBILITY
        # ------------------------------------------

        patient_responsibility = (
            procedure_cost
            - insurance_payment
        )

        # ------------------------------------------
        # STORE RESULT
        # ------------------------------------------

        procedure_results.append({

            "procedure_code":
                procedure_code,

            "procedure_name":
                coverage.procedure_name,

            "procedure_cost":
                round(
                    procedure_cost,
                    2
                ),

            "coverage_percentage":
                coverage.coverage_percentage,

            "coverage_status":
                coverage_status,

            "coverage_message":
                coverage_message,

            "frequency_status":
                frequency_status,

            "frequency_message":
                frequency_message,

            "frequency_limit":
                coverage.frequency_limit,

            "times_used":
                coverage.times_used,

            "deductible_applied":
                round(
                    deductible_applied,
                    2
                ),

            "estimated_insurance_payment":
                round(
                    insurance_payment,
                    2
                ),

            "estimated_patient_responsibility":
                round(
                    patient_responsibility,
                    2
                )
        })

        # ------------------------------------------
        # UPDATE TOTALS
        # ------------------------------------------

        total_cost += procedure_cost

        total_insurance_payment += (
            insurance_payment
        )

        total_patient_responsibility += (
            patient_responsibility
        )

    # ------------------------------------------
    # OVERALL STATUS
    # ------------------------------------------

    failed_procedures = [

        result

        for result in procedure_results

        if (
            result["coverage_status"] == "FAIL"
            or
            result["frequency_status"] == "FAIL"
        )
    ]

    if policy.status != "Active":

        overall_status = "NOT ELIGIBLE"

    elif len(failed_procedures) > 0:

        overall_status = "NOT ELIGIBLE"

    else:

        overall_status = "ELIGIBLE"

    # ------------------------------------------
    # FINAL RESULT
    # ------------------------------------------

    return {

        "overall_status":
            overall_status,

        "procedure_count":
            len(procedure_results),

        "total_procedure_cost":
            round(
                total_cost,
                2
            ),

        "total_estimated_insurance_payment":
            round(
                total_insurance_payment,
                2
            ),

        "total_estimated_patient_responsibility":
            round(
                total_patient_responsibility,
                2
            ),

        "procedures":
            procedure_results
    }