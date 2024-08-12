from src.app.client import auth_client
from src.app.schemas.auth_schemas import TokenSchema
from fastapi import HTTPException, status


async def check_token_dependency(token_data: TokenSchema) -> TokenSchema:
    """Проверка токена."""
    token_response = await auth_client.post(
        endpoint='check_token/',
        json=token_data.model_dump()
    )
    if token_response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=token_response.status_code,
            detail=token_response.json()['detail']
        )
    return token_data
