import httpx
from fastapi import APIRouter, status

from app.schemas.auth_schemas import UserRegister

router = APIRouter(tags=["registration"])


# TODO Сделать пути через переменные settings pydantic
@router.post("/registration/", status_code=status.HTTP_200_OK)
async def auth(user_req: UserRegister):
    """Проксирует запрос на регестрацию."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="http://0.0.0.0:8000/registration/", json=user_req.model_dump()
        )
    return response.json()
