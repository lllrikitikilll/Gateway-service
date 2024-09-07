from fastapi import APIRouter, Response
from opentracing import global_tracer

from src.app.client import auth_client
from src.app.core.settings import settings
from src.app.schemas.auth_schemas import UserAuth, UserRegister

router = APIRouter(tags=["auth"])
router = APIRouter(
    tags=["auth"],
    prefix=settings.url.root_prefix,
)


@router.post("/registration/")
async def registration(
    user_req: UserRegister, response: Response
) -> dict:
    """Проксирует запрос на регистрацию."""
    with global_tracer().start_active_span("registration") as scope:
        scope.span.set_tag("login", user_req.login)
        response_client = await auth_client.post(
            endpoint="registration/",
            json=user_req.model_dump(),
            span_ctx=scope.span.context
        )
        response.status_code = response_client.status_code
        scope.span.set_tag("response_status", response.status_code)
    return response_client.json()


@router.post("/auth/")
async def auth(
    user_req: UserAuth, response: Response
) -> dict:
    """Проксирует запрос на авторизацию."""
    with global_tracer().start_active_span("auth") as scope:
        scope.span.set_tag("user_id", user_req.login)
        response_client = await auth_client.post(
            endpoint="auth/",
            json=user_req.model_dump(),
            span_ctx=scope.span.context
        )

        response.status_code = response_client.status_code
        scope.span.set_tag("user_token", user_req.token)
        scope.span.set_tag("response_status", response.status_code)
        scope.span.set_tag("access_token", response_client.json().get("token"))
    return response_client.json()
