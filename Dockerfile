# syntax=docker/dockerfile:1.7-labs

FROM python:3.11.9-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    python -m pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

COPY . .


FROM python:3.11.9-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/app/.local/bin:${PATH}"

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --create-home app

COPY --from=builder /wheels /wheels
RUN --mount=type=cache,target=/root/.cache \
    python -m pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

COPY --chown=app:app . .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" >/dev/null 2>&1 || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
