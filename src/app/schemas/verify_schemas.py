from pydantic import BaseModel

from src.app.schemas.auth_schemas import TokenSchema


class VerifySchema(BaseModel):
    """Схема запроса на верификацию."""

    user_id: int
    path: str


class ReportRequest(BaseModel):
    """Схема запроса списка транзакции с токеном."""

    token: TokenSchema
    verify: VerifySchema
