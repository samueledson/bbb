from sqlalchemy import Column, Boolean, Integer, String

from app.database.session import Base


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    program_season = Column(String, nullable=False)
    form_section = Column(String, nullable=False)
    question_text = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False)
