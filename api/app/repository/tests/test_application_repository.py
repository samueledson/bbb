from copy import copy
from unittest.mock import Mock

from app.database.models.application_model import ApplicationModel
from app.repository.application_repository import ApplicationRepository

# Testes unitários para o repositório de inscrições

def test_get_all_by_candidate_id():
    # Cria um mock de ApplicationModel
    application_record = ApplicationModel(
        id=1,
        candidate_id=1,
        program_season="BBB24",
        country_region="SUDESTE",
        video_url="1234567890",
        photo1_url="1234567890",
        photo2_url="1234567890",
        photo3_url="1234567890",
        status="ENTREGUE",
    )

    # Cria outro mock de ApplicationModel
    application_record2 = copy(application_record)
    application_record2.id = 2
    application_record2.candidate_id = 2

    # Cria um mock do banco de dados
    db_mock = Mock()

    # Configura o mock para retornar uma lista com os dois mocks de ApplicationModel
    db_mock.query.return_value.filter.return_value.all.return_value = [application_record, application_record2]

    # Cria um mock do repositório
    repository = ApplicationRepository(db_mock)

    # Chama a função get_all_by_candidate_id com o id do candidato
    all_applications = repository.get_all_by_candidate_id(1)

    # Verifica se a função all foi chamada apenas uma vez
    db_mock.query.return_value.filter.return_value.all.assert_called_once()

    # Verifica se a lista retornada contém o número correto de inscrições
    assert len(all_applications) == 2

    # Verifica se a lista retornada contém as inscrições corretas
    assert all_applications[0] == application_record
    assert all_applications[1] == application_record2


def test_soft_delete():
    # Cria um mock de ApplicationModel
    application = ApplicationModel(
        id=1,
        candidate_id=1,
        program_season="BBB24",
        country_region="SUDESTE",
        status="ENTREGUE",
        deleted_at=None
    )

    # Cria um mock do banco de dados
    db_mock = Mock()
    db_mock.query.return_value.filter.return_value.first.return_value = application

    # Cria um mock do repositório
    repository = ApplicationRepository(db_mock)

    # Chama a função soft_delete com o id da inscrição
    repository.soft_delete(application.id)

    # Verifica se o campo deleted_at foi preenchido
    assert application.deleted_at is not None

    # Verifica se o banco de dados foi atualizado
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(application)
