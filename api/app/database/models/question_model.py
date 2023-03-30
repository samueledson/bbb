from sqlalchemy import Column, Boolean, Integer, Text, Enum

from app.database.session import Base
from app.types.form_section import FS_FormSection
from app.types.program_season import PS_ProgramSeason


class QuestionModel(Base):
    """
    Modelo de tabela para as questões.
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    program_season = Column(Enum(PS_ProgramSeason), nullable=False)
    form_section = Column(Enum(FS_FormSection), nullable=False)
    question_text = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, index=True)
