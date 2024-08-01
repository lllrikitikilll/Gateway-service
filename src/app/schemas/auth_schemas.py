from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    """Схема запроса пользователя."""

    login: str
    password: str


class UserAuth(UserRegister):
    """Схема запроса аутентификации."""

    token: Optional[str] = None


class User(BaseModel):
    """Схема пользователя."""

    login: str
    hash_password: str
    id: Optional[int] = None


class TokenSchema(BaseModel):
    """Схема токена пользователя."""

    user_id: int
    token: str
