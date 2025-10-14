# STRIDE Threat Model — FastAPI Wishes App

## Контекст

Сервис: **FastAPI + PostgreSQL + JWT + внешний Price API**
Цель: выявить угрозы по STRIDE для потоков F1–F10 и связать их с контролями (NFR из P03).

---

## Таблица STRIDE-угроз

| Поток/Элемент | Угроза (STRIDE) | Риск | Контроль / Мера | Связь с NFR | Проверка / Артефакт |
|----------------|-----------------|------|------------------|--------------|----------------------|
| F1 Login / CRUD | S — Spoofing (подмена клиента) | R1 | JWT-аутентификация, Argon2id, Rate Limit | NFR-01, NFR-03, NFR-04 | e2e тест / ZAP baseline |
| F1 Login / CRUD | T — Tampering (подмена данных) | R2 | HTTPS (TLS 1.3), подпись JWT | NFR-04 | CI security scan |
| F2 Validate JWT | R — Repudiation (отрицание действий) | R3 | Audit trail при входе | NFR-07 | Логирование событий |
| F2 Validate JWT | I — Information Disclosure (утечка данных) | R4 | Маскирование ошибок и логов | NFR-02, NFR-08 | pytest + audit log check |
| F3 ORM Queries | T — Tampering (инъекции SQL) | R5 | SQLAlchemy ORM, Pydantic схемы | NFR-03 | Bandit, pytest |
| F4 SQL over TLS | I — Information Disclosure | R6 | Шифрование соединения, доступ по ролям | NFR-04 | DB config / CI scan |
| F5 Audit Logs | R — Repudiation | R7 | Audit logs с user_id | NFR-07 | Проверка логов / e2e |
| F5 Audit Logs | I — Information Disclosure (PII) | R8 | Маскирование данных | NFR-08 | pytest логов / CI |
| F6 External Price API | E — Elevation of Privilege | R9 | Валидация ответа внешнего API | NFR-04 | Postman / e2e |
| F7 JSON Response | T — Tampering (внешние данные) | R10 | Проверка схемы JSON | NFR-04 | Contract test |
| F8 HTTPS Response | I — Information Disclosure | R11 | Маскирование ошибок (RFC7807) | NFR-02 | ZAP baseline |
| F9/F10 Auth Failure | D — Denial of Service | R12 | Rate Limit, Retry Timeout | NFR-05 | Нагрузочный тест (Locust 50 RPS) |

---

## Обоснование покрытия

- Покрыто **12 угроз** (≥12 → ★★ уровень).
- Каждая угроза связана с **конкретным NFR**.
- Проверки интегрированы в **CI, pytest, e2e**.
- Исключения (физический доступ, инфраструктура) не рассматриваются.

---

## STRIDE → NFR связь

| Категория STRIDE | Реализующие NFR |
|------------------|-----------------|
| S — Spoofing | NFR-01, NFR-03, NFR-04 |
| T — Tampering | NFR-03, NFR-04 |
| R — Repudiation | NFR-07 |
| I — Information Disclosure | NFR-02, NFR-08 |
| D — Denial of Service | NFR-05 |
| E — Elevation of Privilege | NFR-04 |
