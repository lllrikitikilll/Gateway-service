import time

from fastapi import FastAPI, Request
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)
from prometheus_client import make_asgi_app

from src.app.api.auth_router import router as auth_router
from src.app.api.healthz.healthz_router import router as healthz_router
from src.app.api.transaction_router import router as transaction_router
from src.app.api.verify_router import router as verify_router
from src.app.metrics.prometheus_metric import REQUEST_COUNT, REQUEST_DURATION

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(verify_router)
app.include_router(healthz_router)


def get_service_name(path: str) -> str:
    """Получение имени сервиса по его пути."""
    service_mapping = {
        "auth-service": ["/api/auth", "/api/registration"],
        "transactions-service": ["/api/transaction", "/api/report"],
        "verify-service": ["/api/verify"],
    }

    for service_name, paths in service_mapping.items():
        if any(sp in path for sp in paths):
            return service_name

    return "None"


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware для сбора метрик сервиса."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    service_name = get_service_name(request.url.path)
    REQUEST_DURATION.labels(
        method=request.method, service=service_name, endpoint=request.url.path
    ).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        service=service_name,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    return response


@app.middleware("http")
async def tracing_middleware(request: Request, call_next):
    """Трассирование запроса через разные сервисы."""
    path = request.url.path
    if (  # noqa: WPS337
        path.startswith("/healthz/live")
        or path.startswith("/healthz/ready")  # noqa: W503
        or path.startswith("/metrics")  # noqa: W503
    ):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS, request.headers
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f"apanin_gateway_{request.method}_{path}",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response
