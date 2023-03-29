from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.database.models.application_model import ApplicationModel
from app.database.models.question_model import QuestionModel
from app.repository.answer_repository import AnswerRepository
from app.repository.application_repository import ApplicationRepository
from app.repository.candidate_repository import CandidateRepository
from app.schemas.application_schema import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationService:
    """
    Serviço para as inscrições.
    """
    def __init__(self, db: Session):
        self.db = db
        self.repository = ApplicationRepository(db)
        self.repository_candidate = CandidateRepository(db)

    def get_all_by_candidate_id(self, candidate_id: int) -> List[ApplicationModel]:
        self.validate_candidate(candidate_id=candidate_id)
        return self.repository.get_all_by_candidate_id(candidate_id=candidate_id)

    def create(self, application: ApplicationCreateSchema) -> ApplicationModel:
        self.validate_candidate(candidate_id=application.candidate_id)
        db_application = self.repository.get_by_candidate_id(candidate_id=application.candidate_id)
        if db_application:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Já existe uma inscrição para este candidato na temporada informada")
        return self.repository.create(application)

    def update(self, application_id: int, application: ApplicationUpdateSchema) -> ApplicationModel:
        self.validate_application(application_id=application_id)
        return self.repository.update(application_id=application_id, application=application)

    def delete(self, application_id: int) -> dict[str, str]:
        self.validate_application(application_id=application_id)
        self.repository.soft_delete(application_id=application_id)
        return {"message": "Inscrição removido com sucesso"}

    def get_answers(self, application_id: int) -> List[QuestionModel]:
        self.validate_application(application_id=application_id)
        return AnswerRepository(self.db).get_all_by_application_id(application_id=application_id)

    def validate_candidate(self, candidate_id: int) -> None:
        db_candidate = self.repository_candidate.get_by_id(candidate_id=candidate_id)
        if db_candidate is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Candidato não encontrado")

    def validate_application(self, application_id: int) -> None:
        db_application = self.repository.get_by_id(application_id=application_id)
        if db_application is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

