from datetime import datetime

from pydantic import BaseModel

from src.app.schemas.validators import positiv_int


class TransactionScheme(BaseModel):
    """Схема транзакции."""

    user_id: int
    amount: positiv_int
    operation: str = "debit"


class TransactionSchemeResponse(TransactionScheme):
    """Схема ответа транзакции."""

    timestamp: datetime


class ReportQuery(BaseModel):
    """Схема запроса транзакций."""

    user_id: int
    from_date: datetime
    to_date: datetime
