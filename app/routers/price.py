from fastapi import APIRouter, Query

router = APIRouter(prefix="/price", tags=["price"])


@router.get("/")
async def get_price(query: str = Query(..., description="Product name")):
    # Пример - просто фейковая цена
    fake_price = round(len(query) * 1.23, 2)
    return {"query": query, "estimated_price": fake_price}
