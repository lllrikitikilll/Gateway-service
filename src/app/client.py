import httpx
from fastapi import HTTPException, status
from opentracing import Format, global_tracer

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

    async def post(  # noqa: WPS211
        self,
        endpoint: str,
        json: dict | None = None,
        files: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
        span_ctx=None
    ) -> httpx.Response:
        """Работа с POST методами."""
        url = f"{self.base_url}/{endpoint}"
        if span_ctx is not None:
            headers = {}
            global_tracer().inject(span_ctx, Format.HTTP_HEADERS, headers)
        return await self.client.post(
            url, json=json, files=files, data=data, headers=headers
        )

    async def is_ready(self) -> bool:
        """Проверка готовности сервера."""
        try:
            response = await self.client.get(f"{self.base_url}/healthz/live")
        except httpx.ConnectError:
            return False
        return response.status_code == status.HTTP_200_OK


transaction_client = HttpxClient(base_url=settings.url.transaction)
auth_client = HttpxClient(base_url=settings.url.auth)
