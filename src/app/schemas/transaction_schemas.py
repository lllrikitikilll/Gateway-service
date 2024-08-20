from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.app.schemas.auth_schemas import TokenSchema
from src.app.schemas.validators import positiv_int



class TransactionOperation(Enum):
    """Варианты выбора операции транзакции."""

    DEBIT: str = "debit"
    WITHDRAW: str = "withdraw"


class TransactionScheme(BaseModel):
    """Схема транзакции."""

    user_id: int
    amount: positiv_int
    operation: str = "debit"


class TransactionSchemeResponse(TransactionScheme):
    """Схема ответа транзакции."""

    timestamp: datetime


class TransactionRequest(BaseModel):
    """Схема запроса транзакции с токеном."""

    token: TokenSchema
    transaction: TransactionScheme




class ReportQuery(BaseModel):
    """Схема запроса транзакций."""

    user_id: int
    from_date: datetime
    to_date: datetime
