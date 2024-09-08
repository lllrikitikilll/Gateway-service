import datetime
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from opentracing import global_tracer
from src.app.main import app
from src.app.schemas.auth_schemas import TokenSchema


@pytest.fixture
def client():
    """Клиент для теста приложения."""
    return TestClient(app)


@pytest.fixture
def mock_auth(mocker):
    """Мок клиента авторизации."""
    return mocker.patch("src.app.client.auth_client.post", new_callable=AsyncMock)


@pytest.fixture
def mock_transaction(mocker):
    """Мок клиента транзакций."""
    return mocker.patch(
        "src.app.client.transaction_client.post", new_callable=AsyncMock
    )


@pytest.fixture(scope="session")
def span_ctx():
    """Фикстура контектса трасера"""
    with global_tracer().start_active_span("test") as scope:
        return scope.span.context


@pytest.mark.asyncio
async def test_registration(client, mock_auth, span_ctx):
    """Тест для проверки регистрации."""
    mock_auth.return_value = Mock(
        status_code=status.HTTP_200_OK, json=lambda: {"token": "valid_token"}
    )

    response = client.post(
        "api/registration/",
        json={"login": "test_user", "password": "test_pass"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"token": "valid_token"}
    mock_auth.assert_awaited_once_with(
        endpoint="registration/",
        json={"login": "test_user", "password": "test_pass"},
        span_ctx=span_ctx
    )


@pytest.mark.asyncio
async def test_auth(client, mock_auth, span_ctx):
    """Тест авторизации пользователя."""
    mock_auth.return_value = Mock(
        status_code=status.HTTP_200_OK, json=lambda: {"token": "valid_token"}
    )

    response = client.post(
        "api/auth/",
        json={"login": "test_user", "password": "test_pass", "token": "valid_token"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"token": "valid_token"}
    mock_auth.assert_awaited_once_with(
        endpoint="auth/",
        json={
            "login": "test_user",
            "password": "test_pass",
            "token": "valid_token",
        },
        span_ctx=span_ctx
    )


async def test_transactions(client, mock_transaction, mock_auth, span_ctx):
    """Тест отправки транзакции с валидным токеном."""
    transaction_data = {
        "transaction": {"user_id": 1, "amount": 100, "operation": "debit"},
        "token_data": {"user_id": 1, "token": "valid_token"},
    }
    mock_auth.return_value = Mock(status_code=status.HTTP_200_OK)
    mock_transaction.return_value = Mock(
        status_code=status.HTTP_200_OK, json=lambda: {"message": "Операция выполнена"}
    )

    response = client.post("api/transaction/", json=transaction_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Операция выполнена"}
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=transaction_data["token_data"],
        span_ctx=span_ctx
    )
    mock_transaction.assert_awaited_once_with(
        endpoint="create_transaction/", json=transaction_data["transaction"],
        span_ctx=span_ctx
    )


async def test_report(client, mock_transaction, mock_auth, span_ctx):
    """Тест отправки запроса на отчет с валидным токеном."""
    from_date = datetime.datetime.now().isoformat()
    to_date = datetime.datetime.now().isoformat()
    report_query = {
        "report": {
            "user_id": 1,
            "from_date": from_date,
            "to_date": to_date,
        },
        "token_data": {"user_id": 1, "token": "valid_token"},
    }
    timestamp = datetime.datetime.utcnow()
    transaction = {
        'user_id': 1,
        'amount': 10,
        'operation': "debit",
        'timestamp': timestamp
    }
    transaction_response = transaction.copy()
    transaction_response['timestamp'] = timestamp.isoformat()
    mock_auth.return_value = Mock(status_code=status.HTTP_200_OK)
    mock_transaction.return_value = Mock(
        status_code=status.HTTP_200_OK, json=lambda: [transaction],
        span_ctx=span_ctx
    )

    response = client.post("api/report/", json=report_query)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [transaction_response]
    # Проверка что запрос проверки токена выполнялся
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=report_query["token_data"],
        span_ctx=span_ctx
    )
    # Проверка что запрос отчета выполнился
    mock_transaction.assert_awaited_once_with(
        endpoint="get_report/", json=report_query["report"],
        span_ctx=span_ctx
    )


async def test_report_error(client, mock_transaction, mock_auth, span_ctx):
    """
    Тест запроса транзакций с невалидным токеном.

    Транзакция не пройдет при отсутствии валидного токена.
    """
    transaction_data = {
        "transaction": {"user_id": 1, "amount": 100, "operation": "debit"},
        "token_data": {"user_id": 1, "token": "invalid_token"},
    }
    mock_auth.return_value = Mock(
        status_code=status.HTTP_401_UNAUTHORIZED,
        json=lambda: {"detail": "Неверные данные пользователя или токен"},
    )
    mock_transaction.return_value = {"message": "Операция выполнена"}

    response = client.post("api/transaction/", json=transaction_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Неверные данные пользователя или токен"
    # Проверка что запрос проверки токена выполнялся
    mock_auth.assert_awaited_once_with(
        endpoint="check_token/", json=transaction_data["token_data"],
        span_ctx=span_ctx
    )
    # Проверка что запрос транзакции не выполнялся
    mock_transaction.assert_not_awaited()
