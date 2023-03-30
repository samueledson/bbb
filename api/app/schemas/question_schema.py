from pydantic import BaseModel

from app.types.form_section import FS_FormSection
from app.types.program_season import PS_ProgramSeason


class QuestionBaseSchema(BaseModel):
    """
    Esquema base para uma questão.
    """

    program_season: PS_ProgramSeason  # temporada do programa em que a questão será usada
    form_section: FS_FormSection  # seção do formulário em que a questão será exibida
    question_text: str  # texto da pergunta
    is_active: bool  # indica se a questão está ativa ou não


class QuestionSchema(QuestionBaseSchema):
    """
    Esquema para uma questão com ID.
    """

    id: int  # identificador único da questão

    class Config:
        orm_mode = True
