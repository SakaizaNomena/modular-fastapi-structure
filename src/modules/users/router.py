from fastapi import APIRouter, Depends

from .service import UserService
from .dependencies import user_service
from .schema import UserCreate, UserResponse, UserUpdate
from typing import List


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(user_service)
):
    return await service.create(data)


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    offset: int = 0, 
    limit: int = 10,
    service: UserService = Depends(user_service)
):
    return await service.find_all_users(offset, limit)



@router.get("/email", response_model=UserResponse)
async def get_user_by_email(
    email: str = "",
    service: UserService = Depends(user_service)
):
    return await service.find_all_users_by_mail(email)


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    id: int,
    service: UserService = Depends(user_service)
):
    return await service.find_user_by_id(id)



# @router.get("/user_count")
# async def get_user_count(
#     service: UserService = Depends(user_service)
# ):
#     return await service.get_count()


@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    data: UserUpdate,
    service: UserService = Depends(user_service)
):
    return await service.update_user(
        user_id = id,
        name = data.name,
        email = data.email
    )


@router.delete("/{id}", response_model=bool)
async def delete_user(
    id: int,
    service: UserService = Depends(user_service)
):
    return await service.delete_users(id)



