from datetime import datetime

from pydantic import BaseModel

from src.app.schemas.auth_schemas import TokenSchema


class TransactionQuery(BaseModel):
    """Схема запроса транзакций."""

    user_id: int
    from_date: datetime
    to_date: datetime


class ReportRequest(BaseModel):
    """Схема запроса на список транзакций."""

    token: TokenSchema
    query: TransactionQuery
