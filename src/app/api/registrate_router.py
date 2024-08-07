import httpx
from fastapi import APIRouter, status

from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserRegister
from src.app.api.client import HttpxClient


client = HttpxClient(base_url=settings.url.auth)
router = APIRouter(tags=["registration"])


@router.post("/registration/")
async def auth(user_req: UserRegister) -> dict:
    """Проксирует запрос на регистрацию."""
    response = await client.post(
        endpoint='registration/', 
        data=user_req.model_dump()
    )
    return response
