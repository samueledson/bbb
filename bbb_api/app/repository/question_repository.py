from typing import List

from sqlalchemy.orm import Session

from app.database.models.question_model import QuestionModel
from app.types.program_season import PS_ProgramSeason


class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, question_id: int) -> QuestionModel:
        """
        Retorna uma questão pelo seu ID.

        Args:
            question_id (int): ID da questão.

        Returns:
            QuestionModel: objeto de modelo da questão.
        """
        return self.db.query(QuestionModel).filter(QuestionModel.id == question_id, QuestionModel.is_active).first()

    def get_all_by_program_season(self, program_season: PS_ProgramSeason) -> List[QuestionModel]:
        """
        Retorna uma lista de todas as questões para uma temporada de programa.

        Args:
            program_season (ProgramSeason): temporada do programa.

        Returns:
            List[QuestionModel]: lista de objetos de modelo de questão.
        """
        if not isinstance(program_season, PS_ProgramSeason):
            raise TypeError("O parâmetro program_season deve ser do tipo ProgramSeason")

        return self.db.query(QuestionModel).filter(QuestionModel.program_season == program_season,
                                                   QuestionModel.is_active).all()
