from unittest.mock import AsyncMock, Mock
import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.schemas.transaction_schemas import TransactionRequest, TransactionOperation
import datetime


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_auth(mocker):
    mock = mocker.patch("src.app.api.client.auth_client.post", new_callable=AsyncMock)
    return mock


@pytest.fixture
def mock_transaction(mocker):
    mock = mocker.patch(
        "src.app.api.client.transaction_client.post", new_callable=AsyncMock
    )
    return mock


@pytest.mark.asyncio
async def test_registration(client, mock_auth):
    """Тест для проверки регистрации."""
    mock_auth.return_value = Mock(
        status_code=200, json=lambda: {"token": "valid_token"}
    )

    response = client.post(
        "/registration/", json={"login": "test_user", "password": "test_pass"}
    )

    assert response.status_code == 200
    assert response.json() == {"token": "valid_token"}
    mock_auth.assert_awaited_once_with(
        endpoint="registration/",
        json={"login": "test_user", "password": "test_pass"},
    )


@pytest.mark.asyncio
async def test_auth(client, mock_auth):
    """Тест авторизации пользователя."""
    mock_auth.return_value = Mock(
        status_code=200, json=lambda: {"token": "valid_token"}
    )

    response = client.post(
        "/auth/",
        json={"login": "test_user", "password": "test_pass", "token": "valid_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"token": "valid_token"}
    mock_auth.assert_awaited_once_with(
        endpoint="auth/",
        json={
            "login": "test_user",
            "password": "test_pass",
            "token": "valid_token",
        },
    )


async def test_transactions(client, mock_transaction, mock_auth):
    """Тест отправки транзакции с валидным токеном."""
    transaction_data = {
        "transaction": {"user_id": 1, "amount": 100, "operation": "debit"},
        "token": {"user_id": 1, "token": "valid_token"},
    }

    mock_auth.return_value = Mock(
        status_code=200, json=lambda: {"message": "Операция выполнена"}
    )
    mock_transaction.return_value = Mock(
        status_code=200,
        json=lambda: {"message": "Операция выполнена"}
    )

    response = client.post("/transaction/", json=transaction_data)

    transaction_data_copy = transaction_data["transaction"]
    transaction_data_copy["user_id"] = transaction_data["token"]["user_id"]
    transaction_data_copy["operation"] = transaction_data_copy["operation"].lower()

    assert response.status_code == 200
    assert response.json() == {"message": "Операция выполнена"}
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=transaction_data["token"]
    )
    mock_transaction.assert_awaited_once_with(
        endpoint="create_transaction/", json=transaction_data_copy
    )


async def test_report(client, mock_transaction, mock_auth):
    """Тест отправки запроса на отчет с валидным токеном."""
    from_date = datetime.datetime.now().isoformat()
    to_date = datetime.datetime.now().isoformat()
    report_query = {
        "query": {
            "user_id": 1,
            "from_date": from_date,
            "to_date": to_date,
        },
        "token": {"user_id": 1, "token": "valid_token"},
    }
    mock_auth.return_value = Mock(
        status_code=200,
        json=lambda: {"message": "Операция выполнена"}
    )
    mock_transaction.return_value = Mock(
        status_code=200,
        json=lambda: {"message": "Операция выполнена"}
    )

    response = client.post("/report/", json=report_query)
    report_query_copy = report_query["query"]
    report_query_copy["user_id"] = report_query["token"]["user_id"]

    assert response.status_code == 200
    assert response.json() == {"message": "Операция выполнена"}
    # Проверка что запрос проверки токена выполнялся
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=report_query["token"]
    )
    # Проверка что запрос отчета выполнился
    mock_transaction.assert_awaited_once_with(
        endpoint="get_report/", json=report_query_copy
    )


async def test_report_error(client, mock_transaction, mock_auth):
    """
    Тест запроса транзакций с невалидным токеном.

    Транзакция не пройдет при отсутствии валидного токена.
    """
    transaction_data = {
        "transaction": {"user_id": 1, "amount": 100, "operation": "debit"},
        "token": {"user_id": 1, "token": "invalid_token"},
    }
    mock_auth.return_value = Mock(
        status_code=401,
        json=lambda: {"detail": "Неверные данные пользователя или токен"},
    )
    mock_transaction.return_value = {"message": "Операция выполнена"}

    response = client.post("/transaction/", json=transaction_data)

    assert response.status_code == 401
    assert response.json() == {
        "detail": {"detail": "Неверные данные пользователя или токен"}
    }
    # Проверка что запрос проверки токена выполнялся
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=transaction_data["token"]
    )
    # Проверка что запрос транзакции не выполнялся
    mock_transaction.assert_not_awaited()
