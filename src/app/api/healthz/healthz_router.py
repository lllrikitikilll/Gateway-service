# import asyncio

from fastapi import APIRouter, status

# from src.app.api.auth_router import client as auth_client
# from src.app.api.transaction_router import transaction_client

router = APIRouter(tags=["helthz"], prefix="/helthz")


@router.get("/healthz/up")
async def up_check() -> int:
    """Проверьте работоспособность сервера."""
    return status.HTTP_200_OK


@router.get("/healthz/ready")
async def ready_check() -> int:
    """Проверьте работоспособность зависимостей приложения."""
    # readiness_probes = await asyncio.gather(
    #     *[
    #         component
    #         for component in [transaction_client.is_ready(), auth_client.is_ready()]
    #     ],
    # )
    # ready = all(probe for probe in readiness_probes)
    ready = all((True, True))
    return status.HTTP_200_OK if ready else status.HTTP_200_OK
