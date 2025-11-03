from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class WishBase(BaseModel):
    title: str
    link: Optional[str] = None
    price_estimate: Optional[Decimal] = None
    notes: Optional[str] = None


class WishCreate(WishBase):
    pass


class WishUpdate(WishBase):
    pass


class WishRead(WishBase):
    id: int
    user_id: int

    model_config = dict(from_attributes=True)
