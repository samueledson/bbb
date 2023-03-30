from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.answer_schema import AnswerSchema, AnswerCreateSchema, AnswerUpdateSchema
from app.schemas.application_schema import ApplicationSchema, ApplicationCreateSchema, ApplicationUpdateSchema
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["Inscrições"],
)


@router.post(
    "/",
    response_model=ApplicationSchema,
    name="Criar inscrição",
    description="Rota para criar uma inscrição"
)
async def create_application(application: ApplicationCreateSchema, db: Session = Depends(get_db)) -> ApplicationSchema:
    return ApplicationService(db).create(application=application)


@router.put(
    "/{application_id}",
    response_model=ApplicationSchema,
    name="Atualizar inscrição",
    description="Rota para atualizar uma inscrição"
)
async def update_candidate(application_id: int, application: ApplicationUpdateSchema, db: Session = Depends(get_db)) -> ApplicationSchema:
    return ApplicationService(db).update(application_id=application_id, application=application)


@router.delete(
    "/{application_id}",
    name="Remover inscrição",
    description="Rota para deletar uma inscrição"
)
async def delete_candidate(application_id: int, db: Session = Depends(get_db) ):
    return ApplicationService(db).delete(application_id=application_id)


@router.get(
    "/{application_id}/answers",
    response_model=List[AnswerSchema],
    name="Obter respostas por inscrição",
    description="Rota para retornar todas as respostas de uma inscrição"
)
async def read_answer_by_application(application_id: int, db: Session = Depends(get_db)) -> List[AnswerSchema]:
    return ApplicationService(db).get_answers(application_id=application_id)


@router.post(
    "/{application_id}/answers",
    response_model=List[AnswerSchema],
    name="Salvar respostas por inscrição",
    description="Rota para salvar respostas de uma inscrição"
)
async def save_answer_by_application(application_id: int, answers: List[AnswerCreateSchema], db: Session = Depends(get_db)) -> List[AnswerSchema]:
    return ApplicationService(db).save_answers(application_id, answers)
