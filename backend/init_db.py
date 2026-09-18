from .database import engine, SessionLocal, Base
from .models import Patient, Policy, Coverage


# Create all database tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()


# Clear existing test data
db.query(Coverage).delete()
db.query(Policy).delete()
db.query(Patient).delete()


# =========================================================
# PATIENT 1
# SmileCare Insurance
# Active insurance - Good general coverage
# =========================================================

patient1 = Patient(
    name="John Mathew",
    dob="2003-05-12",
    member_id="SCI-10001",
    provider="SmileCare Insurance"
)

policy1 = Policy(
    member_id="SCI-10001",
    status="Active",
    start_date="2026-01-01",
    end_date="2026-12-31",
    annual_limit=1500,
    remaining_limit=920,
    deductible=300,
    deductible_remaining=75
)

coverage1 = [
    Coverage(
        member_id="SCI-10001",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="SCI-10001",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=80,
        frequency_limit=3,
        times_used=1
    ),
    Coverage(
        member_id="SCI-10001",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="SCI-10001",
        procedure_code="D3310",
        procedure_name="Root Canal Treatment",
        coverage_percentage=70,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="SCI-10001",
        procedure_code="D7140",
        procedure_name="Simple Tooth Extraction",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=0
    )
]


# =========================================================
# PATIENT 2
# DentalShield
# Active insurance - Partial coverage
# =========================================================

patient2 = Patient(
    name="Sarah Thomas",
    dob="2002-09-24",
    member_id="DSH-20001",
    provider="DentalShield"
)

policy2 = Policy(
    member_id="DSH-20001",
    status="Active",
    start_date="2026-03-01",
    end_date="2027-02-28",
    annual_limit=2000,
    remaining_limit=1200,
    deductible=500,
    deductible_remaining=200
)

coverage2 = [
    Coverage(
        member_id="DSH-20001",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=50,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="DSH-20001",
        procedure_code="D0210",
        procedure_name="Full Mouth X-rays",
        coverage_percentage=80,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="DSH-20001",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=70,
        frequency_limit=3,
        times_used=1
    ),
    Coverage(
        member_id="DSH-20001",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=50,
        frequency_limit=1,
        times_used=0
    )
]


# =========================================================
# PATIENT 3
# HealthDent
# Expired insurance
# =========================================================

patient3 = Patient(
    name="Arjun Kumar",
    dob="2001-11-08",
    member_id="HD-30001",
    provider="HealthDent"
)

policy3 = Policy(
    member_id="HD-30001",
    status="Expired",
    start_date="2025-01-01",
    end_date="2025-12-31",
    annual_limit=1000,
    remaining_limit=0,
    deductible=250,
    deductible_remaining=250
)

coverage3 = [
    Coverage(
        member_id="HD-30001",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=0,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="HD-30001",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=0,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="HD-30001",
        procedure_code="D3310",
        procedure_name="Root Canal Treatment",
        coverage_percentage=0,
        frequency_limit=1,
        times_used=0
    )
]


# =========================================================
# PATIENT 4
# PrimeDental Insurance
# Active insurance - Cleaning frequency limit reached
# =========================================================

patient4 = Patient(
    name="Emily Joseph",
    dob="2004-02-17",
    member_id="PDI-40001",
    provider="PrimeDental Insurance"
)

policy4 = Policy(
    member_id="PDI-40001",
    status="Active",
    start_date="2026-01-01",
    end_date="2026-12-31",
    annual_limit=1800,
    remaining_limit=600,
    deductible=400,
    deductible_remaining=0
)

coverage4 = [
    Coverage(
        member_id="PDI-40001",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=2
    ),
    Coverage(
        member_id="PDI-40001",
        procedure_code="D0274",
        procedure_name="Bitewing Dental X-rays",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="PDI-40001",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=80,
        frequency_limit=3,
        times_used=1
    )
]


# =========================================================
# PATIENT 5
# SmileCare Insurance
# Active insurance - Low annual maximum remaining
# =========================================================

patient5 = Patient(
    name="Rahul Nair",
    dob="2000-07-19",
    member_id="SCI-10002",
    provider="SmileCare Insurance"
)

policy5 = Policy(
    member_id="SCI-10002",
    status="Active",
    start_date="2026-01-01",
    end_date="2026-12-31",
    annual_limit=1500,
    remaining_limit=150,
    deductible=300,
    deductible_remaining=50
)

coverage5 = [
    Coverage(
        member_id="SCI-10002",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=70,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="SCI-10002",
        procedure_code="D3310",
        procedure_name="Root Canal Treatment",
        coverage_percentage=60,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="SCI-10002",
        procedure_code="D7140",
        procedure_name="Simple Tooth Extraction",
        coverage_percentage=70,
        frequency_limit=2,
        times_used=1
    )
]


# =========================================================
# PATIENT 6
# DentalShield
# Active insurance - Deductible not met
# =========================================================

patient6 = Patient(
    name="Ananya Menon",
    dob="2003-12-05",
    member_id="DSH-20002",
    provider="DentalShield"
)

policy6 = Policy(
    member_id="DSH-20002",
    status="Active",
    start_date="2026-04-01",
    end_date="2027-03-31",
    annual_limit=2500,
    remaining_limit=2100,
    deductible=500,
    deductible_remaining=450
)

coverage6 = [
    Coverage(
        member_id="DSH-20002",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=80,
        frequency_limit=3,
        times_used=1
    ),
    Coverage(
        member_id="DSH-20002",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="DSH-20002",
        procedure_code="D3310",
        procedure_name="Root Canal Treatment",
        coverage_percentage=80,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="DSH-20002",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=70,
        frequency_limit=2,
        times_used=0
    )
]


# =========================================================
# PATIENT 7
# HealthDent
# Active insurance - Specific procedure not covered
# =========================================================

patient7 = Patient(
    name="David George",
    dob="1999-03-28",
    member_id="HD-30002",
    provider="HealthDent"
)

policy7 = Policy(
    member_id="HD-30002",
    status="Active",
    start_date="2026-01-15",
    end_date="2026-12-31",
    annual_limit=1800,
    remaining_limit=1400,
    deductible=350,
    deductible_remaining=100
)

coverage7 = [
    Coverage(
        member_id="HD-30002",
        procedure_code="D9999",
        procedure_name="Other Dental Services",
        coverage_percentage=0,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="HD-30002",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="HD-30002",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=80,
        frequency_limit=3,
        times_used=0
    ),
    Coverage(
        member_id="HD-30002",
        procedure_code="D7140",
        procedure_name="Simple Tooth Extraction",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=0
    )
]


# =========================================================
# PATIENT 8
# PrimeDental Insurance
# Active insurance - Excellent coverage
# =========================================================

patient8 = Patient(
    name="Maya Joseph",
    dob="2002-06-11",
    member_id="PDI-40002",
    provider="PrimeDental Insurance"
)

policy8 = Policy(
    member_id="PDI-40002",
    status="Active",
    start_date="2026-01-01",
    end_date="2026-12-31",
    annual_limit=3000,
    remaining_limit=2800,
    deductible=250,
    deductible_remaining=0
)

coverage8 = [
    Coverage(
        member_id="PDI-40002",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="PDI-40002",
        procedure_code="D0210",
        procedure_name="Full Mouth X-rays",
        coverage_percentage=100,
        frequency_limit=1,
        times_used=0
    ),
    Coverage(
        member_id="PDI-40002",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=90,
        frequency_limit=3,
        times_used=0
    ),
    Coverage(
        member_id="PDI-40002",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=90,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="PDI-40002",
        procedure_code="D3310",
        procedure_name="Root Canal Treatment",
        coverage_percentage=80,
        frequency_limit=1,
        times_used=0
    )
]


# =========================================================
# PATIENT 9
# SmileCare Insurance
# Pending / future insurance
# =========================================================

patient9 = Patient(
    name="Adil Hassan",
    dob="2001-10-30",
    member_id="SCI-10003",
    provider="SmileCare Insurance"
)

policy9 = Policy(
    member_id="SCI-10003",
    status="Pending",
    start_date="2026-10-01",
    end_date="2027-09-30",
    annual_limit=2000,
    remaining_limit=2000,
    deductible=400,
    deductible_remaining=400
)

coverage9 = [
    Coverage(
        member_id="SCI-10003",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=0
    ),
    Coverage(
        member_id="SCI-10003",
        procedure_code="D2391",
        procedure_name="Composite Dental Filling",
        coverage_percentage=80,
        frequency_limit=3,
        times_used=0
    ),
    Coverage(
        member_id="SCI-10003",
        procedure_code="D2740",
        procedure_name="Dental Crown",
        coverage_percentage=70,
        frequency_limit=2,
        times_used=0
    )
]


# =========================================================
# PATIENT 10
# DentalShield
# Active insurance - Annual maximum exhausted
# =========================================================

patient10 = Patient(
    name="Nikhil Varma",
    dob="1998-08-22",
    member_id="DSH-20003",
    provider="DentalShield"
)

policy10 = Policy(
    member_id="DSH-20003",
    status="Active",
    start_date="2026-01-01",
    end_date="2026-12-31",
    annual_limit=1200,
    remaining_limit=0,
    deductible=300,
    deductible_remaining=0
)

coverage10 = [
    Coverage(
        member_id="DSH-20003",
        procedure_code="D2750",
        procedure_name="Porcelain Fused to Metal Crown",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="DSH-20003",
        procedure_code="D1110",
        procedure_name="Routine Dental Cleaning",
        coverage_percentage=100,
        frequency_limit=2,
        times_used=1
    ),
    Coverage(
        member_id="DSH-20003",
        procedure_code="D7140",
        procedure_name="Simple Tooth Extraction",
        coverage_percentage=80,
        frequency_limit=2,
        times_used=0
    )
]


# =========================================================
# ADD ALL DATA
# =========================================================

patients = [
    patient1, patient2, patient3, patient4, patient5,
    patient6, patient7, patient8, patient9, patient10
]

policies = [
    policy1, policy2, policy3, policy4, policy5,
    policy6, policy7, policy8, policy9, policy10
]

coverages = (
    coverage1 + coverage2 + coverage3 + coverage4 + coverage5
    + coverage6 + coverage7 + coverage8 + coverage9 + coverage10
)


db.add_all(patients)
db.add_all(policies)
db.add_all(coverages)

db.commit()
db.close()


print("Database created successfully!")
print("10 sample patients inserted.")
print(f"{len(coverages)} dental procedure coverage records inserted.")