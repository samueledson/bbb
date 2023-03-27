from typing import List, Union
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.application_model import ApplicationModel
from app.repository.application_repository import ApplicationRepository
from app.schemas.application_schema import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ApplicationRepository(db)

    def get_all_by_candidate_id(self, candidate_id: int) -> List[ApplicationModel]:
        return self.repository.get_all_by_candidate_id(candidate_id=candidate_id)

    def create(self, application: ApplicationCreateSchema) -> ApplicationModel:
        db_application = self.repository.get_by_candidate_id(candidate_id=application.candidate_id)
        if db_application:
            raise HTTPException(status_code=400, detail="Já existe uma inscrição para este candidato")
        return self.repository.create(application)

    def update(self, application_id: int, application: ApplicationUpdateSchema) -> ApplicationModel:
        db_application = self.repository.get_by_id(application_id=application_id)
        if db_application is None:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")
        return self.repository.update(application_id=application_id, application=application)

    def delete(self, application_id: int) -> dict[str, str]:
        db_application = self.repository.get_by_id(application_id=application_id)
        if db_application is None:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")
        self.repository.soft_delete(application_id=application_id)
        return {"message": "Inscrição removido com sucesso"}
