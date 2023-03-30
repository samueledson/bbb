from sqlalchemy import Column, Integer, String, Enum, Date, Float, DateTime, func

from app.database.session import Base
from app.types.gender import Gender


class CandidateModel(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    father_name = Column(String(100))
    mother_name = Column(String(100))
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(String(45), nullable=False)
    religion = Column(String(45))
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(45), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
