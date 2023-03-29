from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository.candidate_repository import CandidateRepository
from app.schemas.application_schema import ApplicationSchema
from app.schemas.candidate_schema import CandidateSchema, CandidateCreateSchema, CandidateUpdateSchema
from app.services.candidate_service import CandidateService

router = APIRouter(
    prefix="/candidates",
    tags=["Candidatos"]
)


@router.get(
    "/",
    response_model=List[CandidateSchema],
    name="Obter todos os candidatos",
    description="Rota para obter todos os registros de candidatos"
)
async def read_candidates(skip: int = None, limit: int = None, db: Session = Depends(get_db)) -> List[CandidateSchema]:
    candidate_repository = CandidateRepository(db)
    all_candidates = candidate_repository.get_all(skip, limit)
    return all_candidates


@router.get(
    "/{candidate_id}",
    response_model=CandidateSchema,
    name="Obter candidato",
    description="Rota para obter um candidato específico"
)
async def read_candidate(candidate_id: int, db: Session = Depends(get_db)) -> CandidateSchema:
    candidate_service = CandidateService(db)
    candidate = candidate_service.get_one(candidate_id)
    return candidate


@router.post(
    "/",
    response_model=CandidateSchema,
    name="Criar candidato",
    description="Rota para criar um candidato"
)
async def create_candidate(candidate: CandidateCreateSchema, db: Session = Depends(get_db)) -> CandidateSchema:
    candidate_service = CandidateService(db)
    candidate = candidate_service.create(candidate)
    return candidate


@router.put(
    "/{candidate_id}",
    name="Atualizar candidato",
    response_model=CandidateSchema,
    description="Rota para atualizar um candidato específico"
)
async def update_candidate(candidate_id: int, candidate: CandidateUpdateSchema, db: Session = Depends(get_db)) -> CandidateSchema:
    candidate_service = CandidateService(db)
    candidate = candidate_service.update(candidate_id, candidate)
    return candidate


@router.delete(
    "/{candidate_id}",
    name="Remover candidato",
    description="Rota para remover um candidato específico"
)
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate_service = CandidateService(db)
    message = candidate_service.delete(candidate_id)
    return message


@router.get(
    "/{candidate_id}/applications",
    response_model=List[ApplicationSchema],
    name="Obter todas as inscrições por candidato",
    description="Rota para obter todas as inscrições de um candidato específico"
)
async def read_applications_by_candidate(candidate_id: int, db: Session = Depends(get_db)) -> List[ApplicationSchema]:
    candidate_service = CandidateService(db)
    all_applications = candidate_service.get_applications(candidate_id)
    return all_applications

