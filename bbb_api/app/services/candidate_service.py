from typing import List, Union
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.application_model import ApplicationModel
from app.database.models.candidate_model import CandidateModel
from app.repository.application_repository import ApplicationRepository
from app.repository.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import CandidateCreateSchema, CandidateUpdateSchema


class CandidateService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CandidateRepository(db)

    def get_all(self, skip: Union[int] = None, limit: Union[int] = None) -> List[CandidateModel]:
        return self.repository.get_all(skip=skip, limit=limit)

    def create(self, candidate: CandidateCreateSchema) -> CandidateModel:
        db_candidate = self.repository.get_by_cpf_or_email(cpf=candidate.cpf, email=candidate.email)
        if db_candidate:
            raise HTTPException(status_code=400, detail="Já existe um cadastro com este CPF ou e-mail")
        return self.repository.create(candidate)

    def update(self, candidate_id: int, candidate: CandidateUpdateSchema) -> CandidateModel:
        db_candidate = self.repository.get_by_id(candidate_id=candidate_id)
        if db_candidate is None:
            raise HTTPException(status_code=404, detail="Candidato não encontrado")
        return self.repository.update(candidate_id=candidate_id, candidate=candidate)

    def delete(self, candidate_id: int) -> dict[str, str]:
        db_candidate = self.repository.get_by_id(candidate_id=candidate_id)
        if db_candidate is None:
            raise HTTPException(status_code=404, detail="Candidato não encontrado")
        self.repository.soft_delete(candidate_id=candidate_id)
        return {"message": "Candidato removido com sucesso"}

    def get_applications(self, candidate_id: int) -> List[ApplicationModel]:
        db_candidate = self.repository.get_by_id(candidate_id=candidate_id)
        if db_candidate is None:
            raise HTTPException(status_code=404, detail="Candidato não encontrado")
        return ApplicationRepository(self.db).get_all_by_candidate_id(candidate_id=candidate_id)

