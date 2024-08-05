import httpx
from fastapi import APIRouter, status

from app.core.settings import settings
from app.schemas.auth_schemas import UserAuth

router = APIRouter(tags=["auth"])


@router.post("/auth/", status_code=status.HTTP_200_OK)
async def auth(user_req: UserAuth):
    """Проксирует запрос на авторизацию."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.url.auth}/auth/", json=user_req.model_dump()
        )
    return response.json()
