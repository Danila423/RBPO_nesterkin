# SecDev Course Template

![CI/CD](https://github.com/Danila423/RBPO_nesterkin/actions/workflows/ci.yml/badge.svg?branch=main)


## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
uvicorn app.main:app --reload
```

## Ритуал перед PR
```bash
ruff check --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## Тесты
```bash
pytest -q
```

## CI/CD
Workflow `.github/workflows/ci.yml` запускается на push и pull_request в матрице Python 3.11/3.12,
кэширует pip, выполняет `ruff`, `black --check`, `isort --check-only`, `pytest` с покрытием и сохраняет
отчёты (`reports/`) артефактами. При успешном push в `main` выполняется мок-деплой в окружение
`staging`, что эмулирует CD-промоушн.

## Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```
## Entities

`User(id, username, email, password_hash)`

`Wish(id, user_id, title, link, price_estimate, notes)`

## Эндпойнты

- `GET /wishes`              - прочитать
- `GET /wishes/{id}`         - прочитать по id
- `POST /wishes?name=...`    - создать
- `PUT /wishes/{id}`        - обновить
- `DELETE /wishes/{id}`      - удалить
- `GET /price`               - получить цену



## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

## Требования безопасности

| Категория           | Реализация                                                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Аутентификация**      | ≥5 неуспешных логинов за 5 мин → блокировка 10 мин; ответ унифицирован (403/401 без уточнения); событие `account_lockout` фиксируется.                             |
| **Сессии**              | Срок жизни access-токена ≤ 15 мин; idle-timeout 30 мин; при смене пароля — отзыв всех сессий ≤ 2 мин; сессии привязаны к device_fingerprint.                       |
| **Сессии (доп.)**       | При выходе пользователя (`logout`) активная сессия удаляется из хранилища, чтобы токен нельзя было использовать повторно.                                         |
| **Ошибки / ответы**     | Ответы аутентификации и валидации однотипные (401/403 без раскрытия причин); поля email/телефон маскированы в логах.                                             |
| **Секреты**             | API-ключи и пароли хранятся только в secrets manager; ротация ≤ 90 дней; аудит `secret_access`; secret-scan = 0 в репозитории и рантайме.                        |
| **Логи / аудит**        | ≥95% критичных действий (создание/удаление Wish, смена пароля) порождают событие `audit{actor, action, resource, result, correlation_id}` ≤ 5 сек.                |
| **Логи / аудит (доп.)** | Логи хранятся не менее 30 дней и доступны только администраторам или службе безопасности.                                   |
| **Приватность / ретеншн** | Храним только минимально-необходимые поля ; маскирование ПДн; удаление данных >30 дней при отсутствии обязательств. |




См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.
