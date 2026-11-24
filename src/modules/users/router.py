from fastapi import APIRouter, Depends

from .service import UserService
from .dependencies import get_user_service
from .schema import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create(data)
