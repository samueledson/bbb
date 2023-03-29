from typing import List, Optional

from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session

from app.database.models.answer_model import AnswerModel
from app.schemas.answer_schema import AnswerCreateSchema, AnswerUpdateSchema


class AnswerRepository:
    """
    Repositório para as respostas.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_application_id(self, application_id: int) -> List[AnswerModel]:
        """
        Retorna todas as respostas de uma inscrição.
        """
        return self.db.query(AnswerModel).filter(
            AnswerModel.application_id == application_id
        ).all()

    def get_by_id(self, answer_id: int) -> Optional[AnswerModel]:
        """
        Retorna uma resposta por ID.
        """
        try:
            return self.db.query(AnswerModel).filter(
                AnswerModel.id == answer_id
            ).one()
        except NoResultFound:
            return None

    def get_by_application_and_question(self, application_id: int, question_id: int) -> Optional[AnswerModel]:
        """
        Retorna uma resposta por inscrição e pergunta.
        """
        try:
            return self.db.query(AnswerModel).filter(
                AnswerModel.application_id == application_id,
                AnswerModel.question_id == question_id
            ).one()
        except NoResultFound:
            return None

    def create(self, answer: AnswerCreateSchema) -> AnswerModel:
        """
        Cria uma nova resposta.
        """
        db_answer = AnswerModel(**answer.dict())
        self.db.add(db_answer)
        try:
            self.db.commit()
            self.db.refresh(db_answer)
        except IntegrityError:
            self.db.rollback()
            raise
        return db_answer

    def update(self, answer_id: int, answer: AnswerUpdateSchema) -> Optional[AnswerModel]:
        """
        Atualiza uma resposta existente.
        """
        db_answer = self.get_by_id(answer_id)
        if db_answer:
            for key, value in answer.dict(exclude_unset=True).items():
                setattr(db_answer, key, value)
            try:
                self.db.commit()
                self.db.refresh(db_answer)
            except IntegrityError:
                self.db.rollback()
                raise
            return db_answer
        else:
            return None
