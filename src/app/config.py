from contextlib import asynccontextmanager

from fastapi import FastAPI
from jaeger_client import Config

from src.app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan. Запускает трассировщик Jaeger."""
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': settings.jaeger_agent.jaeger_host,
                'reporting_port': int(settings.jaeger_agent.jaeger_port),
            },
            'logging': True,
        },
        service_name='apanin-gateway-service',
        validate=True,
    )
    tracer = config.initialize_tracer()
    yield {
        'jaeger_tracer': tracer,
    }
