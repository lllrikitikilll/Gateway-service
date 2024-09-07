from fastapi import APIRouter, File, Form, Response, UploadFile

from src.app.client import auth_client
from src.app.core.settings import settings
from src.app.dependency.auth_dependency import check_token_dependency
from src.app.schemas.auth_schemas import TokenSchema

router = APIRouter(
    tags=["verify"],
    prefix=settings.url.root_prefix,
)


@router.post("/verify/")
async def send_data(
    response: Response,
    file: UploadFile = File(...),
    user_id: int = Form(...),
    token: str = Form(...),
) -> dict:
    """Отправляет данные на серверный эндпоинт /verify/."""
    await check_token_dependency(
        token_data=TokenSchema(user_id=user_id, token=token)
    )

    response_verify = await auth_client.post(
        endpoint="verify/",
        files={"file": (file.filename, await file.read(), file.content_type)},
        data={"user_id": user_id, "token": token},
    )
    response.status_code = response_verify.status_code
    return response_verify.json()
