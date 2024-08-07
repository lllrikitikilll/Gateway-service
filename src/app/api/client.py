import httpx
from fastapi import HTTPException, status

class HttpxClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    

    async def get(self, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.get(url, params=kwargs)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )
        return response.json()

    async def post(self, endpoint: str, data: dict = {}) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.post(url, json=data)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )
        return response.json()