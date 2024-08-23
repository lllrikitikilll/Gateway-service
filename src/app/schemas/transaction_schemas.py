from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.app.schemas.auth_schemas import TokenSchema


class User(BaseModel):
    """Схема пользователя."""

    id: int
    verified: bool = False
    balance: Decimal = Decimal(0)


class TransactionOperation(Enum):
    """Варианты выбора операции транзакции."""

    DEBIT: str = "debit"
    WITHDRAW: str = "withdraw"


class Transaction(BaseModel):
    """Схема транзакции."""

    user_id: int
    amount: float
    operation: TransactionOperation


class TransactionDB(Transaction):
    """Схема транзакции."""

    datetime_utc: datetime


class ReportTransaction(BaseModel):
    """Транзакции за период."""

    transactions: Optional[list[Transaction]]


class TransactionRequest(BaseModel):
    """Схема запроса транзакции с токеном."""

    token: TokenSchema
    transaction: Transaction


class TransactionQuery(BaseModel):
    """Схема запроса транзакций."""

    user_id: int
    from_date: datetime
    to_date: datetime


class ReportRequest(BaseModel):
    """Схема запроса на список транзакций."""

    token: TokenSchema
    query: TransactionQuery
