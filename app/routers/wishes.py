from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.wish import Wish
from app.schemas.wish import WishCreate, WishRead, WishUpdate

router = APIRouter(prefix="/wishes", tags=["wishes"])


@router.get("/", response_model=list[WishRead])
async def list_wishes(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Wish]:
    stmt = select(Wish).limit(limit).offset(offset)
    # user видит только свои; admin — все
    if user.role != "admin":
        stmt = stmt.where(Wish.user_id == user.id)
    res = await db.execute(stmt)
    return list(res.scalars().all())


@router.get("/{wish_id}", response_model=WishRead)
async def get_wish(
    wish_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Wish:
    res = await db.execute(select(Wish).where(Wish.id == wish_id))
    wish = res.scalar_one_or_none()
    if not wish:
        raise HTTPException(status_code=404, detail="not_found")
    if user.role != "admin" and wish.user_id != user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    return wish


@router.post("/", response_model=WishRead)
async def create_wish(
    payload: WishCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Wish:
    wish = Wish(
        title=payload.title,
        link=payload.link,
        price_estimate=payload.price_estimate,
        notes=payload.notes,
        user_id=user.id,
    )
    db.add(wish)
    await db.commit()
    await db.refresh(wish)
    return wish


@router.put("/{wish_id}", response_model=WishRead)
async def update_wish(
    wish_id: int,
    payload: WishUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Wish:
    res = await db.execute(select(Wish).where(Wish.id == wish_id))
    wish = res.scalar_one_or_none()
    if not wish:
        raise HTTPException(status_code=404, detail="not_found")
    if user.role != "admin" and wish.user_id != user.id:
        raise HTTPException(status_code=403, detail="forbidden")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(wish, k, v)
    await db.commit()
    await db.refresh(wish)
    return wish


@router.delete("/{wish_id}")
async def delete_wish(
    wish_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, str]:
    res = await db.execute(select(Wish).where(Wish.id == wish_id))
    wish = res.scalar_one_or_none()
    if not wish:
        raise HTTPException(status_code=404, detail="not_found")
    if user.role != "admin" and wish.user_id != user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    await db.delete(wish)
    await db.commit()
    return {"status": "deleted"}
