from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.answer_schema import AnswerUpdateSchema, AnswerCreateSchema, AnswerSchema
from app.services.answer_service import AnswerService

router = APIRouter(
    prefix="/answers",
    tags=["Respostas"]
)


@router.post(
    "/",
    response_model=AnswerSchema,
    name="Criar resposta",
    description="Cria uma nova resposta."
)
async def create_answer(answer: AnswerCreateSchema, db: Session = Depends(get_db)) -> AnswerSchema:
    answer_service = AnswerService(db)
    created_answer = answer_service.create(answer)
    return created_answer


@router.put(
    "/{answer_id}",
    response_model=AnswerSchema,
    name="Atualiza resposta",
    description="Atualiza uma resposta existente."
)
async def update_answer(answer_id: int, answer: AnswerUpdateSchema, db: Session = Depends(get_db)) -> AnswerSchema:
    answer_service = AnswerService(db)
    updated_answer = answer_service.update(answer_id, answer)
    return updated_answer
