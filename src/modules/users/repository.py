from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from .entity import User
from .model import UserModel


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:

        model = UserModel(
            name=user.name,
            email=user.email
        )

        self.session.add(model)
        await self.session.flush()

        return User(
            id=model.id,
            name=model.name,
            email=model.email
        )

    async def find_by_id(self, user_id: int) -> User | None:

        model = await self.session.get(UserModel, user_id)

        if not model:
            return None

        return User(
            id=model.id,
            name=model.name,
            email=model.email
        )


    async def find_by_name(self, name: str) -> User | None: 

        statment = select(UserModel).where(UserModel.name == name)

        result = await self.session.execute(statment)

        model = result.scalar_one_or_none()

        if not model:
            return None

        return User(
            id=model.id,
            name=model.name,
            email=model.email
        )

    async def find_by_email(self, email: str) -> User | None:
        statment = select(UserModel).where(UserModel.email == email)

        result = await self.session.execute(statment)

        model = result.scalar_one_or_none()

        if not model:
            return None

        return User(
            id=model.id,
            email=model.email,
            name=model.name
        )