import httpx
from fastapi import APIRouter, status

from app.core.settings import settings
from app.schemas.auth_schemas import UserRegister

router = APIRouter(tags=["registration"])


@router.post("/registration/", status_code=status.HTTP_200_OK)
async def auth(user_req: UserRegister):
    """Проксирует запрос на регестрацию."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.url.auth}/registration/", json=user_req.model_dump()
        )
    return response.json()
