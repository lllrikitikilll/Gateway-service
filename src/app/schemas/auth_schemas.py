from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    """Схема регистрации пользователя."""

    login: str
    password: str


class UserAuth(UserRegister):
    """Схема аутентификации пользователя."""

    token: Optional[str] = None


class TokenSchema(BaseModel):
    """Схема токена пользователя."""

    user_id: int
    token: str
