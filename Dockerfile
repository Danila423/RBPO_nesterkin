# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
