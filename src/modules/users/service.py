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



    async def find_all_users(self, offset, limit):
        return await self.repository.find_all(offset, limit)
    

    async def find_all_users_by_mail(self, email, offset, limit):
        return await self.repository.find_by_email(email, offset, limit)
    

    async def find_user_by_id(self, user_id):
        return await self.repository.find_by_id(user_id)

    
    async def update_user(self, user_id, name, email):
        return await self.repository.update_user(user_id, name, email)

   
    async def get_count(self): 
        return await self.repository.get_count_all_user()


    async def delete_users(self, user_id):
        return await self.repository.delete_user(user_id)

