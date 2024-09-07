from fastapi import APIRouter, Depends, Response
from opentracing import global_tracer

from src.app.client import transaction_client
from src.app.core.settings import settings
from src.app.dependency.auth_dependency import check_token_dependency
from src.app.schemas.auth_schemas import TokenSchema
from src.app.schemas.transaction_schemas import (
    ReportQuery,
    TransactionScheme,
    TransactionSchemeResponse
)

router = APIRouter(
    tags=["transaction"],
    prefix=settings.url.root_prefix,
)


@router.post("/transaction/")
async def create_transaction(
    transaction: TransactionScheme,
    response: Response,
    token: TokenSchema = Depends(check_token_dependency)
) -> dict:
    """Проксирует запрос на оздание транзакции с проверкой токена."""
    with global_tracer().start_active_span("transaction") as scope:
        scope.span.set_tag("token", token.token[:10])
        scope.span.set_tag("request_data", str(transaction))
        transaction_data = transaction.model_dump()
        transaction_data["user_id"] = token.user_id
        transaction_response = await transaction_client.post(
            endpoint="create_transaction/",
            json=transaction_data,
            span_ctx=scope.span.context
        )
        response.status_code = transaction_response.status_code
        scope.span.set_tag("responce_code", response.status_code)
        return transaction_response.json()


@router.post("/report/")
async def get_report(
    report: ReportQuery,
    response: Response,
    token: TokenSchema = Depends(check_token_dependency),
) -> list[TransactionSchemeResponse]:
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    with global_tracer().start_active_span("report") as scope:
        scope.span.set_tag("token", token.token[:10])
        scope.span.set_tag("request_data", str(report))
        report_data = report.model_dump()
        report_data["user_id"] = token.user_id
        report_data["from_date"] = report_data["from_date"].isoformat()
        report_data["to_date"] = report_data["to_date"].isoformat()

        report_response = await transaction_client.post(
            endpoint="get_report/",
            json=report_data,
            span_ctx=scope.span.context
        )
        response.status_code = report_response.status_code
        return report_response.json()
