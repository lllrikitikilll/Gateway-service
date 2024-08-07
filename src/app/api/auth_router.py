from fastapi import APIRouter, status

from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserAuth
from src.app.api.client import HttpxClient


router = APIRouter(tags=["auth"])
client = HttpxClient(base_url=settings.url.auth)


@router.post("/auth/")
async def auth(user_req: UserAuth) -> dict:
    """Проксирует запрос на авторизацию."""
    response = await client.post(endpoint='auth/', data=user_req.model_dump())
    return response
