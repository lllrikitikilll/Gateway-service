from fastapi import APIRouter

from src.app.api.client import auth_client
from src.app.schemas.auth_schemas import UserAuth, UserRegister

router = APIRouter(tags=["auth"])


@router.post("/registration/")
async def registration(user_req: UserRegister) -> dict:
    """Проксирует запрос на регистрацию."""
    return await auth_client.post(
        endpoint="registration/", post_data=user_req.model_dump()
    )


@router.post("/auth/")
async def auth(user_req: UserAuth) -> dict:
    """Проксирует запрос на авторизацию."""
    return await auth_client.post(endpoint="auth/", post_data=user_req.model_dump())
