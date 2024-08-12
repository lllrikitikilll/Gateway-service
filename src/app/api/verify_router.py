import httpx
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, Form

from src.app.core.settings import settings
from src.app.schemas.verify_schemas import ReportRequest
from src.app.client import auth_client
from src.app.dependency.auth_dependency import check_token_dependency
from src.app.schemas.auth_schemas import TokenSchema

router = APIRouter(tags=["verify"])


@router.post("/verify/")
async def verify(
    file: UploadFile, user_id: int = Form(...), token: str = Form(...)
) -> dict:
    """Проксирует запрос верифиацию по пути к файлу с проверкой токена."""
    token_data = await check_token_dependency(token_data=TokenSchema(
        user_id=user_id,
        token=token
    ))

    verify_response = await auth_client.post(
        endpoint='verify/',
        data=token_data.model_dump(),
        files={'file': (
            file.filename, await file.read(), file.content_type
        )}
    )
    return verify_response.json()
