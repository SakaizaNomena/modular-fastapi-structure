from .entity import User
from .repository import UserRepository
from .schema import UserCreate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, data: UserCreate):

        user = User(
            id=None,
            name=data.name,
            email=data.email
        )

        return await self.repository.create(user)