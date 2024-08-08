from fastapi import APIRouter

from src.app.api.client import HttpxClient
from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserAuth, UserRegister

router = APIRouter(tags=["auth"])
client = HttpxClient(base_url=settings.url.auth)


@router.post("/registration/")
async def registration(user_req: UserRegister) -> dict:
    """Проксирует запрос на регистрацию."""
    return await client.post(endpoint="registration/", data=user_req.model_dump())


@router.post("/auth/")
async def auth(user_req: UserAuth) -> dict:
    """Проксирует запрос на авторизацию."""
    return await client.post(endpoint="auth/", data=user_req.model_dump())
