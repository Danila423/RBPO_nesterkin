# ADR-001: RFC 7807 ошибки + correlation_id

Дата: 2025-11-03

Статус: Accepted

## Context

Сервис должен безопасно обрабатывать ошибки без утечки внутренних деталей, поддерживать трассировку инцидентов и единый контракт для клиентов. Требования зафиксированы в NFR (маскирование деталей, структурированный ответ) и Threat Model (не раскрывать стек/SQL и иметь трассировку для расследований).

## Decision

- Ввести единый формат ошибок RFC 7807 с полями: `type`, `title`, `status`, `detail`, `correlation_id`.
- Добавить middleware, генерирующее `X-Correlation-ID` и прокидывающее `request.state.correlation_id`.
- Назначить глобальные обработчики:
  - HTTPException → RFC7807
  - ValidationError (422) → RFC7807 (+ список ошибок)
  - Любые прочие исключения → 500 RFC7807 с маскированием деталей

Код: `app/core/errors.py`, регистрация в `app/main.py`.

## Consequences

- Плюсы: единый контракт, трассируемость, отсутствие утечек деталей, удобство для логирования.
- Минусы: небольшой оверхед сериализации и поддержки, необходимость обновить тесты на ожидаемый формат.

## Alternatives

- Оставить поведение FastAPI по умолчанию: риск утечек деталей, нет `correlation_id`.
- Свой кастомный формат JSON: не стандарт, хуже совместимость.

## Security impact

- Снижает риск информации Disclosure (STRIDE: Information Disclosure). Маскирует внутренние детали. Улучшает расследуемость через `correlation_id`.

## Rollout plan

- Включено глобально в приложении. Проверка через интеграционные тесты. Backward-compatible на уровне кодов статуса.

## Links

- NFR: `docs/security-nfr/NFR.md` (NFR-03 Ошибки RFC7807)
- Threat Model: `docs/threat-model/STRIDE.md` (Information Disclosure), `docs/threat-model/RISKS.md`
- Тесты: `tests/test_rfc7807.py`
- Коммиты: см. PR p05-secure-coding → main
