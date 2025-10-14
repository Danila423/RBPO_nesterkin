# 🧩 P04 — Data Flow Diagram (DFD)

## 1. Контекст

**Сервис:** Wishes App (FastAPI + PostgreSQL + JWT + роли + внешний Price API)
**Цель:** показать, как данные проходят через систему и где проходят границы доверия.

### Уровни доверия
- **External** — пользователь, клиент (браузер, мобильное приложение).
- **Edge** — слой API (FastAPI), зона аутентификации и бизнес-логики.
- **Core** — внутренние данные (PostgreSQL, секреты, аудит).
- **External Service** — внешний поставщик данных (Price API).

---

## 2. Основная DFD (Mermaid)

# Data Flow Diagram (DFD) — FastAPI Wish Service


```mermaid
flowchart TB

    subgraph CLIENT["Trust Boundary - Client"]
        U["User Client (Browser or Mobile App)"]
    end

    subgraph EDGE["Trust Boundary - Edge (API Layer)"]
        A["FastAPI App - Auth, Wishes, Price Endpoints"]
    end

    subgraph CORE["Trust Boundary - Core (Business Logic)"]
        S["SQLAlchemy ORM"]
    end

    subgraph DATA["Trust Boundary - Data (Persistent Layer)"]
        DB["PostgreSQL Database"]
        LOGS["Audit Logs and Monitoring"]
        SECRETS["Secrets Storage for JWT Keys and DB Creds"]
    end

    subgraph EXT["External Services"]
        PRICE_API["External Price API"]
    end


    U -->|"F1 HTTPS Request - Login or Wishes CRUD"| A
    A -->|"F2 Validate JWT or Argon2id Password"| SECRETS
    A -->|"F3 Query or Update via ORM"| S
    S -->|"F4 SQL over TLS"| DB
    A -->|"F5 Log Event or Error"| LOGS
    A -->|"F6 HTTPS Request to Price API"| PRICE_API
    PRICE_API -->|"F7 JSON Price Response"| A
    A -->|"F8 HTTPS Response with JSON"| U


    U -->|"F9 Invalid Credentials"| A
    A -->|"F10 Unauthorized Response (masked error)"| U
    U -->|F11: Rate Limit Middleware login, register| A
    A -->|F12: RFC7807 Error Response masked| U
    A -->|F13: Global Exception Handling| LOGS

```
