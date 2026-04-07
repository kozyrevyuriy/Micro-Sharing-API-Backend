# Micro-Sharing API (Backend)

## Описание

Backend-сервис для аренды самокатов/велосипедов.
Реализует пользователей, транспортные средства и поездки с защитой от race condition.

## Стек

* FastAPI
* SQLAlchemy
* SQLite

## Функциональность

* Создание пользователей
* Добавление транспортных средств
* Начало поездки (`/rides/start`)
* Завершение поездки (`/rides/end`)

## Ключевые особенности

* Защита от race condition через атомарные UPDATE-запросы
* Гарантия: один самокат не может быть арендован двумя пользователями одновременно
* Гарантия: поездку нельзя завершить дважды
* Бизнес-логика вынесена в service layer (разделение router/service)

## Установка и запуск

```bash
git clone <repo_url>
cd microsharing

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Документация API

После запуска доступна по адресу:

```
http://127.0.0.1:8000/docs
```

## Примеры запросов

### Создание пользователя

POST /users

```json
{
  "email": "test@example.com"
}
```

### Создание транспортного средства

POST /vehicles

```json
{
  "status": "available"
}
```

### Начало поездки

POST /rides/start
Параметры: `user_id`, `vehicle_id`


### Завершение поездки

POST /rides/end
Параметр: `user_id`

## Обработка конкурентности (race condition)

Проблема:
При одновременных запросах несколько пользователей могли арендовать один и тот же самокат.

Решение:
Использован атомарный UPDATE:

```
UPDATE vehicles
SET status = 'in_ride'
WHERE id = ? AND status = 'available'
```

* только один запрос изменяет строку
* остальные получают 0 обновлений и ошибку

Аналогичная логика применена для завершения поездки.

---
