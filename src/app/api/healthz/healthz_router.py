import asyncio

from fastapi import APIRouter, Response, status

from src.app.client import auth_client, transaction_client

router = APIRouter(tags=["healthz"], prefix="/healthz")


@router.get("/live")
async def up_check() -> int:
    """Проверьте работоспособность сервера."""
    return status.HTTP_200_OK


@router.get("/ready")
async def ready_check(responce: Response) -> int:
    """Проверьте работоспособность зависимостей приложения."""
    try:
        readiness_probes = await asyncio.gather(
            transaction_client.is_ready(),
            auth_client.is_ready(),
        )
    except Exception:
        return status.HTTP_503_SERVICE_UNAVAILABLE

    ready = all(readiness_probes)
    if not ready:
        responce.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE
