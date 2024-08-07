from fastapi import APIRouter

from src.app.api.client import HttpxClient
from src.app.core.settings import settings
from src.app.schemas.transaction_schemas import TransactionRequest

router = APIRouter(tags=["transaction"])

transaction_client = HttpxClient(base_url=settings.url.transaction)
auth_client = HttpxClient(base_url=settings.url.auth)


@router.post("/transaction/")
async def auth(request: TransactionRequest) -> dict:
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    await auth_client.post(
        endpoint="check_token/", data=request.token.model_dump()
    )
    request.transaction.user_id = request.token.user_id
    transaction_data = request.transaction.model_dump()
    transaction_data["user_id"] = request.token.user_id
    transaction_data["operation"] = transaction_data["operation"].value
    transaction_response = await transaction_client.post(
        endpoint="create_transaction/",
        data=transaction_data,
    )
    return transaction_response
