from fastapi import HTTPException
from sqlalchemy import Column, ForeignKey, Integer, DateTime, func, Text
from sqlalchemy.orm import validates
from starlette.status import HTTP_400_BAD_REQUEST

from app.database.session import Base


class AnswerModel(Base):
    """
    Modelo de tabela para as respostas.
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    @validates('answer_text')
    def validate_answer_text(self, key, answer_text):
        """
        Valida se a resposta está preenchida e se não excede o limite de caracteres.
        """
        if len(answer_text.strip()) == 0:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='O campo resposta não pode ser vazio.')
        if len(answer_text.strip()) > 255:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='O campo resposta dever ter um tamanho máximo de 255 caracteres.')
        return answer_text
