from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware

from app.core.database import Base, engine
from app.routers import auth, price, wishes

app = FastAPI(title="SecDev Course App", version="0.3.1")

app.add_middleware(SlowAPIMiddleware)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "type": "about:blank",
            "title": "Internal Server Error",
            "detail": "An unexpected error occurred.",
            "instance": str(request.url),
        },
    )


app.include_router(auth.router)
app.include_router(wishes.router)
app.include_router(price.router)
