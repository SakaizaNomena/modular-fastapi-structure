from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db

from .repository import UserRepository
from .service import UserService


def user_service(
    session: AsyncSession = Depends(get_db)
):
    repository = UserRepository(session)

    return UserService(repository)