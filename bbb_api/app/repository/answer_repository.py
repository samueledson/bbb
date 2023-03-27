from typing import List

from sqlalchemy.orm import Session

from app.database.models.answer_model import AnswerModel


class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_application_id(self, application_id: int) -> List[AnswerModel]:
        return self.db.query(AnswerModel).filter(AnswerModel.application_id == application_id).all()


