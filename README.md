Реализован сервис проксирования запросов в отдельные сервисы

### Установка сервиса
```bash
git pull git@hub.mos.ru:shift-python/y2024/homeworks/apanin/gateway_api.git
poetry install --dev

# Устанавливаем подмодули (рекурсивно)
git submodule update --init --recurcive

# Запуск группы сервисов
docker-compose up -d
```

## Описание сервиса

Отвечает за проксирование запросов в сервисы. С помощью `docker-compose` запускается группа контейнеров отвечающих за внешние сервера и дополнительно ПО:
1. Авторизации
2. Транзакций
3. Верификации
4. БД PostgreSQL
5. Kafka И Zookeper


### Запуск линтера flake8:
```bash
poetry run flake8 src/app
```

Запуск mypy:
```bash
poetry run mypy src/app
```