from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class AnswerModel(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    application = relationship("ApplicationModel")
    