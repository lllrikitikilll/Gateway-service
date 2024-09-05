from typing import Final

from prometheus_client import Counter, Histogram

SERVICE_PREFIX: Final[str] = "apanin_gateway"
REQUEST_COUNT = Counter(
    name=f"{SERVICE_PREFIX}_request_count",
    documentation="Total number of requests",
    labelnames=["method", "service", "endpoint", "status"],
)
REQUEST_DURATION = Histogram(
    name=f"{SERVICE_PREFIX}_request_duration",
    documentation="Time spent processing request",
    labelnames=["method", "service", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
