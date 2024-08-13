from fastapi import APIRouter, Depends

from src.app.client import transaction_client
from src.app.dependency.auth_dependency import check_token_dependency
from src.app.schemas.auth_schemas import TokenSchema
from src.app.schemas.transaction_schemas import ReportQuery, Transaction

router = APIRouter(tags=["transaction"])


@router.post("/transaction/")
async def create_transaction(
    transaction: Transaction, token: TokenSchema = Depends(check_token_dependency)
) -> dict:
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    transaction_data = transaction.model_dump()
    transaction_data["user_id"] = token.user_id
    transaction_data["operation"] = transaction_data["operation"].value
    transaction_response = await transaction_client.post(
        endpoint="create_transaction/",
        json=transaction_data,
    )
    return transaction_response.json()


@router.post("/report/")
async def get_report(
    report: ReportQuery, token: TokenSchema = Depends(check_token_dependency)
) -> dict:
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    report_data = report.model_dump()
    report_data["user_id"] = token.user_id
    report_data["from_date"] = report_data["from_date"].isoformat()
    report_data["to_date"] = report_data["to_date"].isoformat()

    report_response = await transaction_client.post(
        endpoint="get_report/", json=report_data
    )
    return report_response.json()
