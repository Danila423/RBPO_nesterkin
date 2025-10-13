from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import auth, price, wishes

app = FastAPI(title="SecDev Course App", version="0.3.0")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(wishes.router)
app.include_router(price.router)
