FROM python:3.12-slim

WORKDIR /usr/src

COPY poetry.lock pyproject.toml ./

RUN python3.12 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

