from fastapi import APIRouter, HTTPException, status

from src.app.client import auth_client
from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserAuth, UserRegister

router = APIRouter(tags=["auth"])
router = APIRouter(
    tags=["auth"],
    prefix=settings.url.root_prefix,
)


@router.post("/registration/")
async def registration(user_req: UserRegister) -> dict:
    """Проксирует запрос на регистрацию."""
    response = await auth_client.post(
        endpoint="registration/", json=user_req.model_dump()
    )
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/auth/")
async def auth(user_req: UserAuth) -> dict:
    """Проксирует запрос на авторизацию."""
    response = await auth_client.post(endpoint="auth/", json=user_req.model_dump())
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
