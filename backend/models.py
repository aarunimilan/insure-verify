from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dob = Column(String)
    member_id = Column(String, unique=True, index=True)
    provider = Column(String)


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, index=True)
    status = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    annual_limit = Column(Float)
    remaining_limit = Column(Float)
    deductible = Column(Float)
    deductible_remaining = Column(Float)


class Coverage(Base):
    __tablename__ = "coverages"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, index=True)
    procedure_code = Column(String)
    procedure_name = Column(String)
    coverage_percentage = Column(Float)
    frequency_limit = Column(Integer)
    times_used = Column(Integer)