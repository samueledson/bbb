from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository.question_repository import QuestionRepository
from app.schemas.question_schema import QuestionSchema
from app.types.program_season import PS_ProgramSeason

router = APIRouter(
    prefix="/questions",
    tags=["Perguntas"]
)


@router.get(
    "/{program_season}",
    response_model=List[QuestionSchema],
    name="Perguntas por temporada do programa",
    description="Retorna todas as perguntas de uma determinada temporada do programa."
)
async def read_questions_by_program_season(program_season: PS_ProgramSeason, db: Session = Depends(get_db)) -> List[QuestionSchema]:
    question_repository = QuestionRepository(db)
    all_questions = question_repository.get_all_by_program_season(program_season)
    return all_questions
