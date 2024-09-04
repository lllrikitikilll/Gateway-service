from fastapi import FastAPI, Request
import time
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)
from src.app.api.auth_router import router as auth_router
from src.app.api.healthz.healthz_router import router as healthz_router
from src.app.api.transaction_router import router as transaction_router
from src.app.api.verify_router import router as verify_router
from prometheus_client import make_asgi_app
from src.app.metrics.prometheus_metric import REQUEST_COUNT, REQUEST_DURATION


app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(verify_router)
app.include_router(healthz_router)


def get_service_name(path: str):
    auth_prefix = '/api/apanin-auth'
    transactions_prefix = '/api/apanin-transaction'
    if path.startswith(auth_prefix):
        service_name = 'auth-service'
    elif path.startswith(transactions_prefix):
        service_name = 'transactions-service'
    else:
        service_name = 'None'
    return service_name


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    service_name = get_service_name(request.url.path)
    REQUEST_DURATION.labels(
        method=request.method,
        service=service_name,
        endpoint=request.url.path
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
    path = request.url.path
    if path.startswith('/up') or path.startswith('/ready') or path.startswith('/metrics'):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(propagation.Format.HTTP_HEADERS, request.headers)
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f"gateway_{request.method}_{path}",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response
