from datetime import date
from pydantic import BaseModel
from app.types.gender import Gender


class CandidateBaseSchema(BaseModel):
    cpf: str
    full_name: str
    birth_date: date
    father_name: str = None
    mother_name: str = None
    gender: Gender
    height: float
    religion: str = None
    email: str


class CandidateCreateSchema(CandidateBaseSchema):
    password: str


class CandidateUpdateSchema(CandidateCreateSchema):
    cpf: str = None
    full_name: str = None
    birth_date: date = None
    gender: Gender = None
    height: float = None
    email: str = None
    password: str = None


class CandidateSchema(CandidateBaseSchema):
    id: int
    # applications: list[Application] = []

    class Config:
        orm_mode = True
        exclude = ("password",)
