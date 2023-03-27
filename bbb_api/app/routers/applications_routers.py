from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.application_schema import ApplicationSchema, ApplicationCreateSchema, ApplicationUpdateSchema
from app.services.application_service import ApplicationService

router = APIRouter()


# Rota para criar uma inscrição
@router.post("/applications", response_model=ApplicationSchema, tags=["applications"])
def create_application(application: ApplicationCreateSchema, db: Session = Depends(get_db)):
    return ApplicationService(db).create(application=application)


# Rota para atualizar uma inscrição
@router.put("/applications/{application_id}", response_model=ApplicationSchema, tags=["applications"])
def update_candidate(application_id: int, application: ApplicationUpdateSchema, db: Session = Depends(get_db)):
    return ApplicationService(db).update(application_id=application_id, application=application)


# Rota para deletar uma inscrição
@router.delete("/applications/{application_id}", tags=["applications"])
def delete_candidate(application_id: int, db: Session = Depends(get_db)):
    return ApplicationService(db).delete(application_id=application_id)

