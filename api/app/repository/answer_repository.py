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

    def get_by_application_id_and_question_id(self, application_id: int, question_id: int) -> Optional[AnswerModel]:
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

    def save(self, application_id: int, answer: AnswerCreateSchema) -> AnswerModel:
        """
        Cria uma nova resposta.
        """
        db_answer = self.get_by_application_id_and_question_id(application_id, answer.question_id)

        if db_answer is None:
            db_answer = AnswerModel(**answer.dict())
            db_answer.application_id = application_id
            self.db.add(db_answer)
        else:
            db_answer.answer = answer.answer_text

        try:
            self.db.commit()
            self.db.refresh(db_answer)
        except IntegrityError:
            self.db.rollback()
            raise
        return db_answer

    # def update(self, application_id: int, answer: AnswerUpdateSchema) -> Optional[AnswerModel]:
    #     """
    #     Atualiza uma resposta existente.
    #     """
    #     db_answer = self.get_by_application_and_question(application_id, answer.question_id)
    #     if db_answer:
    #         for key, value in answer.dict(exclude_unset=True).items():
    #             setattr(db_answer, key, value)
    #         try:
    #             self.db.commit()
    #             self.db.refresh(db_answer)
    #         except IntegrityError:
    #             self.db.rollback()
    #             raise
    #         return db_answer
    #     else:
    #         return None

    def save_answers(self, application_id: int, answers: List[AnswerCreateSchema]) -> List[AnswerModel]:
        """
        Cria várias respostas.
        """
        db_answers = []
        for answer in answers:
            db_answers.append(self.save(application_id, answer))
        return db_answers

    # def update_answers(self, application_id: int, answers: List[AnswerUpdateSchema]) -> List[AnswerModel]:
    #     """
    #     Atualiza várias respostas.
    #     """
    #     db_answers = []
    #     for answer in answers:
    #         db_answers.append(self.update(application_id, answer))
    #     return db_answers
