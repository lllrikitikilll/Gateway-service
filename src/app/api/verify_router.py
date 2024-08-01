import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.verify_schemas import ReportRequest

router = APIRouter(tags=["verify"])


# TODO Сделать пути через переменные settings pydantic
@router.post("/verify/", status_code=status.HTTP_200_OK)
async def verify(request: ReportRequest):
    """Проксирует запрос верифиацию по пути к файлу с проверкой токена."""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            url="http://auth_service:8000/check_token/", json=request.token.model_dump()
        )
        if token_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=token_response.json()["detail"],
            )
        verify_response = await client.post(
            url="http://verify_service:8003/verify/", json=request.verify.model_dump()
        )
    return verify_response.json()
