from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

BLACKLISTED_JTI: set[str] = set()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def create_token(
    data: dict[str, Any],
    minutes: int,
    token_type: str,
) -> str:
    to_encode = data.copy()
    jti = uuid4().hex
    exp = _now() + timedelta(minutes=minutes)
    to_encode.update({"exp": exp, "type": token_type, "jti": jti})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("jti") in BLACKLISTED_JTI:
            return None
        return payload
    except JWTError:
        return None


def blacklist_token_jti(jti: str) -> None:
    BLACKLISTED_JTI.add(jti)
