# FastAPI Template

Шаблон для создания API с использованием FastAPI, SQLAlchemy, Alembic и PostgreSQL.

## 📋 Требования

- Docker и Docker Compose

## 🚀 Быстрый старт

### Запуск через Docker Compose

1. Клонируйте репозиторий:
```bash
git clone https://github.com/KIIGIN/fastapi-template.git
cd fastapi-template
```

2. Создайте файл .env из примера:
```bash
cp .env.example .env
```

3. Запустите проект через Docker Compose:
```bash
docker compose up -d
```

4. Примените миграции:
```bash
# Вариант 1: Через контейнер приложения
docker compose exec app alembic upgrade head

# Вариант 2: Через отдельную команду
docker compose run --rm app alembic upgrade head
```

Теперь API доступно по адресу: http://localhost:8000