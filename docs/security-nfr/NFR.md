# Non-Functional Requirements (Security NFR) — Wish List Service

| ID | Название | Описание | Метрика / Порог | Проверка (чем / где) | Компонент | Приоритет |
|----|-----------|-----------|------------------|-----------------------|------------|------------|
| NFR-01 | Контроль ошибок 5xx | Ошибки 5xx не превышают 0.5% на проде | ≤ 0.5% запросов | pytest + CI отчет | wishes / api | High |
| NFR-02 | Argon2id для хеширования паролей | Используется алгоритм Argon2id для безопасного хранения паролей | t=3, m=65536, p=4 | Unit-тест security.py | auth | High |
| NFR-03 | Короткоживущие access-токены | Access-токен живёт ≤ 15 минут (refresh ≤ 7 дней) | TTL ≤ 15 мин | pytest + JWT decode | auth | High |
| NFR-04 | Таймауты и ретраи внешних API | Все внешние запросы имеют таймаут ≤ 5 с, не более 2 ретраев | timeout ≤ 5s, retries ≤ 2 | Mock-тесты, CI logs | price / external | Medium |
| NFR-05 | Ротация секретов | Все секреты (ключи, токены) ротуются ≤ 90 дней | TTL ≤ 90 дней | CI secret-scan + review | core | Medium |
| NFR-06 | Логирование критичных действий | ≥95% действий типа create/update/delete фиксируются в аудит-логах | audit_coverage ≥ 95% | e2e + log check | wishes / auth | High |
| NFR-07 | Маскирование персональных данных | В логах и ответах маскируются email, токены, пароли | 100% логов без PII | pytest + review логов | core / auth | Medium |
| NFR-08 | Мониторинг уязвимостей зависимостей | High/Critical устраняются ≤ 7 дней | ≤ 7 дней SLA | CI SCA (pip-audit / Dependabot) | build | Medium |
