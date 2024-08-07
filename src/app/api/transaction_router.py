import httpx
from fastapi import APIRouter, HTTPException, status

from app.core.settings import settings
from app.schemas.transaction_schemas import TransactionRequest

router = APIRouter(tags=["transaction"])


@router.post("/transaction/", status_code=status.HTTP_200_OK)
async def auth(request: TransactionRequest):
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            url=f"{settings.url.auth}/check_token/", json=request.token.model_dump()
        )
        if token_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=token_response.status_code, detail=token_response.json()
            )
        request.transaction.user_id = request.token.user_id
        transaction_data = request.transaction.model_dump()
        transaction_data["user_id"] = request.token.user_id
        transaction_data["operation"] = transaction_data["operation"].value
        transaction_response = await client.post(
            url=f"{settings.url.transaction}/create_transaction/",
            json=transaction_data,
        )
    return transaction_response.json()
