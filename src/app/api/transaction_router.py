from fastapi import APIRouter

from src.app.api.auth_router import client as auth_client
from src.app.api.client import HttpxClient
from src.app.core.settings import settings
from src.app.schemas.transaction_schemas import ReportRequest, TransactionRequest

router = APIRouter(tags=["transaction"])

transaction_client = HttpxClient(base_url=settings.url.transaction)


@router.post("/transaction/")
async def transaction(request: TransactionRequest) -> dict:
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    await auth_client.post(endpoint="check_token/", data=request.token.model_dump())
    request.transaction.user_id = request.token.user_id
    transaction_data = request.transaction.model_dump()
    transaction_data["user_id"] = request.token.user_id
    transaction_data["operation"] = transaction_data["operation"].value
    return await transaction_client.post(
        endpoint="create_transaction/",
        data=transaction_data,
    )


@router.post("/report/")
async def report(request: ReportRequest) -> dict:
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    await auth_client.post(endpoint="check_token/", data=request.token.model_dump())
    report_data = request.query.model_dump()
    report_data["user_id"] = request.token.user_id
    report_data["from_date"] = report_data["from_date"].isoformat()
    report_data["to_date"] = report_data["to_date"].isoformat()

    return await transaction_client.post(endpoint="get_report/", data=report_data)
