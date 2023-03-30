from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_401_UNAUTHORIZED

from app.database.models.application_model import ApplicationModel
from app.database.models.candidate_model import CandidateModel
from app.repository.application_repository import ApplicationRepository
from app.repository.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import CandidateCreateSchema, CandidateUpdateSchema
from app.types.program_season import PS_ProgramSeason


class CandidateService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CandidateRepository(db)

    def get_all(self, skip: int = None, limit: int = None) -> List[CandidateModel]:
        all_candidates_record = self.repository.get_all(skip=skip, limit=limit)
        return all_candidates_record

    def get_one(self, candidate_id: int) -> CandidateModel:
        self.validate_candidate(candidate_id)
        candidate_record = self.repository.get_by_id(candidate_id)
        return candidate_record

    def login(self, cpf: str, password: str) -> CandidateModel:
        candidate_exists_record = self.repository.get_by_cpf(cpf)
        if candidate_exists_record is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Candidato não encontrado.")
        candidate_record = self.repository.get_by_cpf_and_password(cpf, password)
        if candidate_record is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="CPF ou Senha fornecidos são inválidos.")
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
            application_repository = ApplicationRepository(self.db)
            application_repository.soft_delete_by_candidate_id(candidate_id)
            message = {"message": "Candidato removido com sucesso"}
            return message
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_application_by_program_season(self, candidate_id: int, program_season: PS_ProgramSeason) -> ApplicationModel:
        self.validate_candidate(candidate_id)
        application_repository = ApplicationRepository(self.db)
        application = application_repository.get_by_candidate_id_and_program_season(candidate_id, program_season)
        if application is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
        return application

    def validate_candidate(self, candidate_id: int) -> None:
        candidate_record = self.repository.get_by_id(candidate_id)
        if candidate_record is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Candidato não encontrado")
