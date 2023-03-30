from pydantic import BaseModel, constr


class AnswerBaseSchema(BaseModel):
    """
    Esquema base de resposta.
    """
    question_id: int
    answer_text: constr(min_length=1, max_length=255)


class AnswerCreateSchema(AnswerBaseSchema):
    """
    Esquema de criação de resposta.
    """
    pass


class AnswerUpdateSchema(AnswerBaseSchema):
    """
    Esquema de atualização de resposta.
    """
    pass


class AnswerSchema(AnswerBaseSchema):
    """
    Esquema de resposta completo.
    """
    id: int
    application_id: int

    class Config:
        orm_mode = True
