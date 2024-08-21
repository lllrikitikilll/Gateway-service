from fastapi import APIRouter

from src.app.api.client import HttpxClient
from src.app.core.settings import settings
from src.app.schemas.report_schemas import ReportRequest

router = APIRouter(tags=["report"])

report_client = HttpxClient(base_url=settings.url.transaction)
auth_client = HttpxClient(base_url=settings.url.auth)


@router.post("/report/")
async def auth(request: ReportRequest) -> dict:
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    await auth_client.post(
        endpoint="check_token/", data=request.token.model_dump()
    )
    report_data = request.query.model_dump()
    report_data["user_id"] = request.token.user_id
    report_data["from_date"] = report_data["from_date"].isoformat()
    report_data["to_date"] = report_data["to_date"].isoformat()

    return await report_client.post(endpoint="get_report/", data=report_data)
