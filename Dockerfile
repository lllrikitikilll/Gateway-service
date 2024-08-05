FROM python:3.12-slim

COPY poetry.lock pyproject.toml ./
COPY /src .
WORKDIR /


RUN python3.12 -m pip install poetry && \
    python3.12 -m poetry install


CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]