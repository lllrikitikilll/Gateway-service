from fastapi import APIRouter, Response

from src.app.client import auth_client
from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserAuth, UserRegister

router = APIRouter(tags=["auth"])
router = APIRouter(
    tags=["auth"],
    prefix=settings.url.root_prefix,
)


@router.post("/registration/")
async def registration(user_req: UserRegister, response: Response) -> dict:
    """Проксирует запрос на регистрацию."""
    response_client = await auth_client.post(
        endpoint="registration/", json=user_req.model_dump()
    )
    response.status_code = response_client.status_code
    return response_client.json()


@router.post("/auth/")
async def auth(user_req: UserAuth, response: Response) -> dict:
    """Проксирует запрос на авторизацию."""
    response_client = await auth_client.post(
        endpoint="auth/", json=user_req.model_dump()
    )
    response.status_code = response_client.status_code
    return response_client.json()
