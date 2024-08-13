import httpx
from fastapi import APIRouter, HTTPException, status

from app.core.settings import settings
from app.schemas.report_schemas import ReportRequest

router = APIRouter(tags=["report"])


@router.post("/report/", status_code=status.HTTP_200_OK)
async def auth(request: ReportRequest):
    """Проксирует запрос на список транзакций за период  с проверкой токена."""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            url=f"{settings.url.auth}/check_token/", json=request.token.model_dump()
        )
        if token_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=token_response.json()["detail"],
            )

        report_data = request.query.model_dump()
        report_data["user_id"] = request.token.user_id
        report_data["from_date"] = report_data["from_date"].isoformat()
        report_data["to_date"] = report_data["to_date"].isoformat()
        report_response = await client.post(
            url=f"{settings.url.transaction}/get_report/", json=report_data
        )
    return report_response.json()
