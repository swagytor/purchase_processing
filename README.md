# Сервис обработки покупок

Сервис обработки покупок предназначен для просмотра товаров, их стоков у различных продавцов, создания заказов с выбранными товарами и бронирования позиций на складе.  

Проект реализован на **Python 3.12** с использованием **FastAPI**, **SQLAlchemy** и других современных библиотек.  

---

## 📦 Основные возможности

- Просмотр списка товаров и их наличия у разных продавцов  
- Создание заказов с выбранными товарами
- Бронирование позиций на складе с возможностью частичного покрытия при недостатке товара в стоке
- Управление данными через SQLAdmin  

---

## 🛠️ Стек технологий

- Python = "^3.12"  
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- python-dotenv
- asyncpg
- pydantic-settings
- uvicorn[standard]
- SQLAdmin
- Pytest + pytest-asyncio для тестирования  
- httpx(для HTTP-запросов)  
- aiosqlite(для SQLite async)  

**Форматирование кода:** `black`, `isort`  
**Линтинг и статический анализ:** `flake8`, `mypy`  

---

## 🚀 Развёртывание

Проект развёрнут с использованием **Docker Compose**.  

### С использованием Make

```bash
# Собрать образы
make build

# Запустить проект
make up
````

### Без Make

```bash
# Собрать образы
docker compose -f docker-compose.yml -p purchase_processing build --no-cache

# Запустить проект
docker compose -f docker-compose.yml -p purchase_processing up --remove-orphans
```

---

## ⚙️ Переменные окружения

Все переменные окружения хранятся в `.env` файле в корневой директории проекта.

Пример `.env`:

```env
PROJECT_NAME=

# Backend
OUTER_PORT=
INNER_PORT=
DEBUG=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

```

---

## 🗄️ Работа с базой данных

* Для создания объектов и управления данными используется **SQLAdmin**.
* Для просмотра админки необходимо перейти по адресу 
* ```bash
  http://0.0.0.0:8000/admin/
  ```
* Миграции базы данных выполняются через **Alembic**.

Пример команды для создания миграций:

```bash
alembic revision --autogenerate -m "Создание таблиц товаров и заказов"
alembic upgrade head
```

---

## 🧪 Тестирование

Для запуска тестов используйте:

```bash
pytest
```
---

## 📝 Swagger / OpenAPI документация

FastAPI автоматически генерирует Swagger UI по адресу:

```bash
http://0.0.0.0:8000/docs
```

Swagger позволяет просматривать все эндпоинты и тестировать API прямо из браузера.

### **Примеры API**
**Получение списка товаров**
```bash
GET /api/items/
```

Ответ:
```bash
[
  {
    "id": 1,
    "title": "Товар 1"
  },
  {
    "id": 2,
    "title": "Товар 2"
  }
]
```

**Получение информации о товаре**
```bash
GET /api/items/{item_id}/
```

Ответ:
```bash
{
  "id": 1,
  "title": "Товар 1",
  "description": "Описание товара",
  "stocks": [
    {
      "id": 1,
      "price": 1000,
      "quantity": 50,
      "available_quantity": 20,
      "item_id": 1
    }
  ]
}
```

**Создание заказа**
```bash
POST /api/orders/
```

```bash
Headers:
  user_id: 1
Body:
{
  "item_id": 1,
  "quantity": 2,
  "max_price": 1200
}
```

Ответ:
```bash
{
  "id": 1,
  "user_id": 1,
  "status": "CREATED",
  "total_quantity": 3,
  "total_price": 2600,
  "order_items": [
    {
      "stock_id": 1,
      "quantity": 2,
      "price": 1000
    },
    {
      "stock_id": 2,
      "quantity": 1,
      "price": 600
    }
  ]
}
```

**Подтверждение заказа**
```bash
POST /api/orders/{order_id}/confirm/
```
```
Headers:
  user-id: 1
```
Ответ:
```bash
{
  "id": 1,
  "user_id": 1,
  "status": "CONFIRMED",
  "total_quantity": 3,
  "total_price": 2600,
  "order_items": [
    {
      "stock_id": 1,
      "quantity": 2,
      "price": 1000
    },
    {
      "stock_id": 2,
      "quantity": 1,
      "price": 600
    }
  ]
}
```
## 📚 Примечания

* Перед запуском убедитесь, что `.env` файл существует и содержит все необходимые переменные.
* Для работы с SQLAdmin нужно подключение к базе данных.
* Docker Compose автоматически создаёт все сервисы (БД, бэкенд ).
* "Аутентификация" выполнена с помощью передачи ID пользователя в Header user_id в связи с упрощённой схемой взаимодействия пользователя с системой


