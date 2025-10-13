from typing import Literal

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: Literal["user", "admin"] = "user"

    model_config = dict(from_attributes=True)
