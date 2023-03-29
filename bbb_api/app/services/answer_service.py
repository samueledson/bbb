from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.database.models.answer_model import AnswerModel
from app.repository.answer_repository import AnswerRepository
from app.repository.application_repository import ApplicationRepository
from app.repository.question_repository import QuestionRepository
from app.schemas.answer_schema import AnswerUpdateSchema, AnswerCreateSchema


class AnswerService:
    """
    Serviço para as respostas.
    """
    def __init__(self, db: Session):
        self.db = db
        self.repository = AnswerRepository(db)
        self.application_repository = ApplicationRepository(db)
        self.question_repository = QuestionRepository(db)

    def create(self, answer: AnswerCreateSchema) -> AnswerModel:
        """
        Cria uma nova resposta.
        """
        self.validate(answer)
        answer_record = self.repository.get_by_application_and_question(
            application_id=answer.application_id,
            question_id=answer.question_id
        )
        if answer_record:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Resposta já existe")
        return self.repository.create(answer=answer)

    def update(self, answer_id: int, answer: AnswerUpdateSchema) -> AnswerModel:
        """
        Atualiza uma resposta existente.
        """
        self.validate(answer)
        answer_record = self.repository.get_by_id(answer_id=answer_id)
        if not answer_record:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Resposta ainda não existe para ser atualizada")
        return self.repository.update(answer_id=answer_id, answer=answer)

    def validate(self, answer: Union[AnswerCreateSchema, AnswerUpdateSchema]) -> None:
        """
        Valida se os dados da resposta são válidos.
        """
        application_record = self.application_repository.get_by_id(application_id=answer.application_id)
        if not application_record:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")
        question_record = self.question_repository.get_by_id(question_id=answer.question_id)
        if not question_record:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pergunta não encontrada")
