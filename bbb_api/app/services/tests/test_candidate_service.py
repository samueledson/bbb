from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import Mock

from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.database.models.candidate_model import CandidateModel
from app.schemas.candidate_schema import CandidateCreateSchema
from app.services.candidate_service import CandidateService

# Testes de integração na camada de serviço (CandidateService)

def test_get_one_candidate():

    # Cria um mock do CandidateModel
    candidate_record = CandidateModel(
        id=1,
        cpf="123.456.789-10",
        full_name="João da Silva",
        birth_date="1990-01-01",
        gender="M",
        height=1.80,
        email="joao.silva@example.com",
        password="123456"
    )

    # Cria um mock do repositório
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = candidate_record
    mock_validate_candidate = Mock()

    # Cria um mock do service
    service = CandidateService(Mock(spec=Session))
    service.repository = mock_repository
    service.validate_candidate = mock_validate_candidate

    # Chama a função get_one do service
    candidate = service.get_one(candidate_record.id)

    # Verifica se o valor retornado é igual ao mock do CandidateModel
    assert candidate == candidate_record

    # Verifica se a função get_by_id foi chamada apenas uma vez
    mock_repository.get_by_id.assert_called_once_with(candidate_record.id)


def test_get_one_candidate_not_found():

    candidate_id = 1

    # Cria um mock do repositório
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = None
    mock_validate_candidate = Mock(side_effect=HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Candidato não encontrado"))

    # Cria um mock do service
    service = CandidateService(Mock(spec=Session))
    service.repository = mock_repository
    service.validate_candidate = mock_validate_candidate

    try:
        # Chama a função get_one do service
        service.get_one(candidate_id)
    except HTTPException as e:
        # Verifica se retornou o status code correto
        assert e.status_code == HTTP_404_NOT_FOUND
        assert e.detail == "Candidato não encontrado"
    else:
        # Se não retornou a exceção, o teste falhou
        assert False, "Exceção HTTPException esperada"


def test_create_candidate():

    # Cria um mock do repositório
    mock_repository = Mock()
    mock_repository.get_by_cpf_or_email.return_value = None
    mock_repository.create.return_value = CandidateModel(
        id=1,
        cpf="123.456.789-10",
        full_name="João da Silva",
        birth_date="1990-01-01",
        gender="M",
        height=1.80,
        email="joao.silva@example.com",
        password="123456"
    )

    # Cria um mock do service
    service = CandidateService(Mock(spec=Session))
    service.repository = mock_repository

    # Cria um mock do CandidateCreateSchema
    candidate = CandidateCreateSchema(
        cpf="123.456.789-10",
        full_name="João da Silva",
        birth_date="1990-01-01",
        gender="M",
        height=1.80,
        email="joao.silva@example.com",
        password="123456"
    )

    # Chama a função create do service
    created_candidate = service.create(candidate)

    # Verifica se o valor retornado é igual ao mock do CandidateModel
    assert created_candidate.id == 1
    assert created_candidate.cpf == "123.456.789-10"
    assert created_candidate.full_name == "João da Silva"
    assert created_candidate.birth_date == "1990-01-01"
    assert created_candidate.gender == "M"
    assert created_candidate.height == 1.80
    assert created_candidate.email == "joao.silva@example.com"
    assert created_candidate.password == "123456"

    # Verifica se as funções get_by_cpf_or_email e create foram chamadas apenas uma vez
    mock_repository.get_by_cpf_or_email.assert_called_once_with(
        cpf=candidate.cpf, email=candidate.email
    )
    mock_repository.create.assert_called_once_with(candidate)


def test_create_candidate_existing_cpf_or_email():

    # Cria um mock do repositório
    mock_repository = Mock()
    mock_repository.get_by_cpf_or_email.return_value = CandidateModel(
        id=1,
        cpf="123.456.789-10",
        full_name="João da Silva",
        birth_date="1990-01-01",
        gender="M",
        height=1.80,
        email="joao.silva@example.com",
        password="123456"
    )

    # Cria um mock do service
    service = CandidateService(Mock(spec=Session))
    service.repository = mock_repository

    # Cria um mock do CandidateCreateSchema
    candidate = CandidateCreateSchema(
        cpf="123.456.789-10",
        full_name="João da Silva",
        birth_date="1990-01-01",
        gender="M",
        height=1.80,
        email="joao.silva@example.com",
        password="123456"
    )

    try:
        # Chama a função create do service
        service.create(candidate)
    except HTTPException as exc:
        # Verifica se retornou o status code correto
        assert exc.status_code == HTTP_400_BAD_REQUEST
        assert exc.detail == "Já existe um cadastro com este CPF ou e-mail"
    else:
        # Se não retornou a exceção, o teste falhou
        assert False, "Exceção HTTPException esperada"
