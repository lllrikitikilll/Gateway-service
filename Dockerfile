FROM python:3.12-slim
# Настройки темы https://github.com/romkatv/powerlevel10k
RUN apt-get update && apt-get install -y curl

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Устанавливаем рабочую директорию


# Копируем файлы проекта в контейнер
COPY poetry.lock pyproject.toml ./
COPY /src .
WORKDIR /
# Устанавливаем зависимости через Poetry
RUN /root/.local/bin/poetry install
CMD ["/root/.local/bin/poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]