from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository.application_repository import ApplicationRepository
from app.repository.candidate_repository import CandidateRepository
from app.schemas.application_schema import ApplicationSchema
from app.schemas.candidate_schema import CandidateSchema, CandidateCreateSchema, CandidateUpdateSchema
from app.services.candidate_service import CandidateService

router = APIRouter()


# Rota para retornar todos os candidatos
@router.get("/candidates", response_model=List[CandidateSchema], tags=["candidates"])
async def read_candidates(skip: Union[int] = None, limit: Union[int] = None, db: Session = Depends(get_db)):
    return CandidateService(db).get_all(skip=skip, limit=limit)


# Rota para retornar um candidato específico
@router.get("/candidates/{candidate_id}", response_model=CandidateSchema, tags=["candidates"])
async def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = CandidateRepository(db).get_by_id(candidate_id=candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidate


# Rota para criar um candidato
@router.post("/candidates", response_model=CandidateSchema, tags=["candidates"])
def create_candidate(candidate: CandidateCreateSchema, db: Session = Depends(get_db)):
    return CandidateService(db).create(candidate=candidate)


# Rota para atualizar um candidato
@router.put("/candidates/{candidate_id}", response_model=CandidateSchema, tags=["candidates"])
def update_candidate(candidate_id: int, candidate: CandidateUpdateSchema, db: Session = Depends(get_db)):
    return CandidateService(db).update(candidate_id=candidate_id, candidate=candidate)


# Rota para deletar um candidato
@router.delete("/candidates/{candidate_id}", tags=["candidates"])
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return CandidateService(db).delete(candidate_id=candidate_id)


# Rota para retornar todas as inscrições de um candidato
@router.get("/candidates/{candidate_id}/applications", response_model=List[ApplicationSchema], tags=["candidates"])
async def read_applications_by_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return CandidateService(db).get_applications(candidate_id=candidate_id)

