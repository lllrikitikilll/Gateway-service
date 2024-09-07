from fastapi import HTTPException, status
from opentracing import global_tracer

from src.app.client import auth_client
from src.app.schemas.auth_schemas import TokenSchema


async def check_token_dependency(token_data: TokenSchema) -> TokenSchema:
    """Проверка токена."""
    with global_tracer().start_active_span("check_token") as scope:
        scope.span.set_tag("user_token", token_data.token[:10])
        scope.span.set_tag("user_id", token_data.user_id)
        token_response = await auth_client.post(
            endpoint="check_token/",
            json=token_data.model_dump(),
            span_ctx=scope.span.context
        )
        scope.span.set_tag("responce_status", token_response.status_code)
        if token_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=token_response.json()["detail"],
            )
        return token_data
