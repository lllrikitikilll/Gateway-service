FROM python:3.12-slim

COPY poetry.lock pyproject.toml ./
COPY /src .
WORKDIR /

ENV APP_CONFIG__url__auth="http://trans_image:8001"
ENV APP_CONFIG__url__transaction="http://auth_image:8002"
ENV APP_CONFIG__url__verification="http://veirfy_image:8003"

RUN python3.12 -m pip install poetry && \
    python3.12 -m poetry install


CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]