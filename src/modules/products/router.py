from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/")
async def get_all_product():
    return []