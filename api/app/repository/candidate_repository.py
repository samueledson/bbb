from datetime import datetime
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database.models.candidate_model import CandidateModel
from app.schemas.candidate_schema import CandidateCreateSchema, CandidateUpdateSchema


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CandidateModel]:
        return self.db.query(CandidateModel).filter(CandidateModel.deleted_at.is_(None)).offset(skip).limit(limit).all()

    def get_by_id(self, candidate_id: int) -> CandidateModel:
        return self.db.query(CandidateModel).filter(CandidateModel.id == candidate_id, CandidateModel.deleted_at.is_(None)).first()

    def get_by_cpf(self, cpf: str) -> CandidateModel:
        return self.db.query(CandidateModel).filter(CandidateModel.deleted_at.is_(None), CandidateModel.cpf == cpf).first()

    def get_by_cpf_or_email(self, cpf: str, email: str) -> CandidateModel:
        return self.db.query(CandidateModel).filter(CandidateModel.deleted_at.is_(None), and_(CandidateModel.cpf == cpf, CandidateModel.email == email)).first()

    def get_by_cpf_and_password(self, cpf: str, password: str) -> CandidateModel:
        return self.db.query(CandidateModel).filter(CandidateModel.deleted_at.is_(None), and_(CandidateModel.cpf == cpf, CandidateModel.password == password)).first()

    def create(self, candidate: CandidateCreateSchema) -> CandidateModel:
        db_candidate = CandidateModel(**candidate.dict())
        self.db.add(db_candidate)
        self.db.commit()
        self.db.refresh(db_candidate)
        return db_candidate

    def update(self, candidate_id: int, candidate: CandidateUpdateSchema) -> CandidateModel | None:
        candidate_record = self.get_by_id(candidate_id)
        if candidate_record:
            for key, value in candidate.dict(exclude_unset=True).items():
                setattr(candidate_record, key, value)
            self.db.commit()
            self.db.refresh(candidate_record)
            return candidate_record
        else:
            return None

    def soft_delete(self, candidate_id: int) -> None:
        candidate_record = self.get_by_id(candidate_id)
        if candidate_record:
            candidate_record.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(candidate_record)

