from fastapi import APIRouter, File, Form, UploadFile

from src.app.client import auth_client
from src.app.dependency.auth_dependency import check_token_dependency
from src.app.schemas.auth_schemas import TokenSchema

router = APIRouter(tags=["verify"])


@router.post("/verify/")
async def send_data(
    file: UploadFile = File(...), user_id: int = Form(...), token: str = Form(...)
) -> dict:
    """Отправляет данные на серверный эндпоинт /verify/."""
    await check_token_dependency(TokenSchema(user_id=user_id, token=token))

    response = await auth_client.post(
        endpoint="verify/",
        files={"file": (file.filename, await file.read(), file.content_type)},
        data={"user_id": user_id, "token": token},
    )

    return response.json()
