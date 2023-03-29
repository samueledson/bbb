from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models.application_model import ApplicationModel
from app.schemas.application_schema import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationRepository:
    """
    Repositório para as inscrições.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_candidate_id(self, candidate_id: int) -> List[ApplicationModel]:
        """
        Retorna todas as inscrições de um candidato.
        """
        return self.db.query(ApplicationModel).filter(
            ApplicationModel.candidate_id == candidate_id,
            ApplicationModel.deleted_at.is_(None)
        ).all()

    def get_by_candidate_id(self, candidate_id: int) -> ApplicationModel:
        """
        Retorna primeira inscrição de um candidato.
        """
        return self.db.query(ApplicationModel).filter(
            ApplicationModel.candidate_id == candidate_id,
            ApplicationModel.deleted_at.is_(None)
        ).first()

    def get_by_id(self, application_id: int) -> ApplicationModel:
        """
        Retorna uma inscrição por ID.
        """
        return self.db.query(ApplicationModel).filter(
            ApplicationModel.id == application_id,
            ApplicationModel.deleted_at.is_(None)
        ).first()

    def create(self, application: ApplicationCreateSchema) -> ApplicationModel:
        """
        Cria uma nova inscrição.
        """
        db_application = ApplicationModel(**application.dict())
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update(self, application_id: int, application: ApplicationUpdateSchema) -> Optional[ApplicationModel]:
        """
        Atualiza uma inscrição existente.
        """
        db_application = self.get_by_id(application_id)
        if db_application:
            for key, value in application.dict(exclude_unset=True).items():
                setattr(db_application, key, value)
            self.db.commit()
            self.db.refresh(db_application)
            return db_application
        else:
            return None

    def soft_delete(self, application_id: int) -> None:
        """
        Realiza a desativação de uma inscrição e mantendo o registro no banco de dados.
        """
        db_application = self.get_by_id(application_id)
        if db_application:
            db_application.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(db_application)
