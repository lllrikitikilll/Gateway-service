from fastapi import APIRouter, HTTPException, status

from src.app.api.client import auth_client, transaction_client
from src.app.schemas.transaction_schemas import ReportRequest, TransactionRequest

router = APIRouter(tags=["transaction"])


@router.post("/transaction/")
async def transaction(request: TransactionRequest) -> dict:
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    response = await auth_client.post(
        endpoint="check_token/", post_data=request.token.model_dump()
    )
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    request.transaction.user_id = request.token.user_id
    transaction_data = request.transaction.model_dump()
    transaction_data["user_id"] = request.token.user_id
    transaction_data["operation"] = transaction_data["operation"].value
    transaction_response = await transaction_client.post(
        endpoint="create_transaction/",
        post_data=transaction_data,
    )
    return transaction_response.json()


@router.post("/report/")
async def report(request: ReportRequest) -> dict:
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    response = await auth_client.post(
        endpoint="check_token/", post_data=request.token.model_dump()
    )
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    report_data = request.query.model_dump()
    report_data["user_id"] = request.token.user_id
    report_data["from_date"] = report_data["from_date"].isoformat()
    report_data["to_date"] = report_data["to_date"].isoformat()

    report_response = await transaction_client.post(
        endpoint="get_report/", post_data=report_data
    )
    return report_response.json()
