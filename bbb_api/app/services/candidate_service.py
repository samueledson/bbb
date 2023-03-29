from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.database.models.application_model import ApplicationModel
from app.database.models.candidate_model import CandidateModel
from app.repository.application_repository import ApplicationRepository
from app.repository.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import CandidateCreateSchema, CandidateUpdateSchema


class CandidateService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CandidateRepository(db)

    def get_one(self, candidate_id: int) -> CandidateModel:
        self.validate_candidate(candidate_id)
        candidate_record = self.repository.get_by_id(candidate_id)
        return candidate_record

    def create(self, candidate: CandidateCreateSchema) -> CandidateModel:
        candidate_record = self.repository.get_by_cpf_or_email(cpf=candidate.cpf, email=candidate.email)
        if candidate_record:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Já existe um cadastro com este CPF ou e-mail")
        candidate_created = self.repository.create(candidate)
        return candidate_created

    def update(self, candidate_id: int, candidate: CandidateUpdateSchema) -> CandidateModel:
        self.validate_candidate(candidate_id)
        candidate_updated = self.repository.update(candidate_id, candidate)
        return candidate_updated

    def delete(self, candidate_id: int):
        self.validate_candidate(candidate_id)
        try:
            self.repository.soft_delete(candidate_id)
            message = {"message": "Candidato removido com sucesso"}
            return message
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_applications(self, candidate_id: int) -> List[ApplicationModel]:
        self.validate_candidate(candidate_id)
        application_repository = ApplicationRepository(self.db)
        all_applications = application_repository.get_all_by_candidate_id(candidate_id)
        return all_applications

    def validate_candidate(self, candidate_id: int) -> None:
        candidate_record = self.repository.get_by_id(candidate_id)
        if candidate_record is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Candidato não encontrado")
