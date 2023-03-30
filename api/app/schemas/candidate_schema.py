from datetime import date
from pydantic import BaseModel
from app.types.gender import Gender


class CandidateBaseSchema(BaseModel):
    cpf: str
    full_name: str
    age: int
    father_name: str = None
    mother_name: str = None
    gender: Gender
    phone: str
    religion: str = None
    email: str

class CandidateLoginSchema(BaseModel):
    cpf: str
    password: str

class CandidateCreateSchema(CandidateBaseSchema):
    password: str


class CandidateUpdateSchema(CandidateCreateSchema):
    cpf: str = None
    full_name: str = None
    age: int = None
    gender: Gender = None
    phone: str = None
    email: str = None
    password: str = None


class CandidateSchema(CandidateBaseSchema):
    id: int
    # applications: list[Application] = []

    class Config:
        orm_mode = True
        exclude = ("password",)
