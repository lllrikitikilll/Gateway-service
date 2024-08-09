import httpx
from fastapi import HTTPException, status

from src.app.core.settings import settings


class HttpxClient:
    """Клиент для работы с сервисами."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get(self, endpoint: str, **kwargs) -> dict:
        """Работа с GET методами."""
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.get(url, params=kwargs)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        return response.json()

    async def post(self, endpoint: str, post_data: dict) -> dict:
        """Работа с POST методами."""
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.post(url, json=post_data)
        return response.json()

    async def is_ready(self) -> bool:
        """Проверка готовности сервера."""
        try:
            response = await self.client.get(self.base_url)
        except httpx.HTTPStatusError:
            return False
        return response.status_code == status.HTTP_200_OK


transaction_client = HttpxClient(base_url=settings.url.transaction)
auth_client = HttpxClient(base_url=settings.url.auth)
