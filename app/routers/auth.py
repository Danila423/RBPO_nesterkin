from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import (
    blacklist_token_jti,
    create_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(
        select(User).where(
            (User.email == user_in.email) | (User.username == user_in.username)
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            (User.email == form.username) | (User.username == form.username)
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_token(
        {"sub": str(user.id), "role": user.role},
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type="access",
    )
    refresh = create_token(
        {"sub": str(user.id), "role": user.role},
        minutes=60 * 24 * 7,
        token_type="refresh",
    )  # 7 дней
    return {"token_type": "bearer", "access_token": access, "refresh_token": refresh}


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="invalid_refresh_token")
    user_id = payload.get("sub")
    role = payload.get("role", "user")
    access = create_token(
        {"sub": user_id, "role": role},
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type="access",
    )
    return {"token_type": "bearer", "access_token": access}


@router.post("/logout")
async def logout(access_token: str):
    payload = decode_token(access_token)
    if not payload:
        raise HTTPException(status_code=400, detail="invalid_token")
    jti = payload.get("jti")
    if jti:
        blacklist_token_jti(jti)
    return {"status": "logged_out"}


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_current_user)):
    return user
