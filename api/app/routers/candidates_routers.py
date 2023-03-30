from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository.candidate_repository import CandidateRepository
from app.schemas.application_schema import ApplicationSchema
from app.schemas.candidate_schema import CandidateSchema, CandidateCreateSchema, CandidateUpdateSchema, \
    CandidateLoginSchema
from app.services.candidate_service import CandidateService
from app.types.program_season import PS_ProgramSeason

router = APIRouter(
    prefix="/candidates",
    tags=["Candidatos"]
)


@router.get(
    "/",
    response_model=List[CandidateSchema],
    name="Obter lista de candidatos",
    description="Rota para obter a listagem com todos os candidatos"
)
async def read_candidates(skip: int = None, limit: int = None, db: Session = Depends(get_db)) -> List[CandidateSchema]:
    candidate_service = CandidateService(db)
    all_candidates = candidate_service.get_all(skip=skip, limit=limit)
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
    "/login",
    response_model=CandidateSchema,
    name="Fazer login",
    description="Rota para fazer login de um candidato"
)
async def login_candidate(candidate: CandidateLoginSchema, db: Session = Depends(get_db)) -> CandidateSchema:
    candidate_service = CandidateService(db)
    candidate = candidate_service.login(candidate.cpf, candidate.password)
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
    "/{candidate_id}/applications/{program_season}",
    response_model=ApplicationSchema,
    name="Obter a inscrição do candidato em uma temporada do programa",
    description="Rota para obter a inscrição de um candidato específico para uma temporada específica do programa"
)
async def read_application_by_candidate_and_program_season(candidate_id: int, program_season: PS_ProgramSeason, db: Session = Depends(get_db)) -> ApplicationSchema:
    candidate_service = CandidateService(db)
    application = candidate_service.get_application_by_program_season(candidate_id, program_season)
    return application

