from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from typing import List
from fastapi import HTTPException
from src.core.exceptions import NotFoundException

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
            raise NotFoundException

        return User(
            id=model.id,
            name=model.name,
            email=model.email
        )


    async def find_by_name(self, name: str, offset: int = 0, limit: int = 10) -> User | None: 

        statment = select(UserModel).offset(offset).limit(limit).where(UserModel.name == name)

        result = await self.session.execute(statment)

        model = result.scalar_one_or_none()

        if not model:
            raise NotFoundException

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
            raise HTTPException(detail="User not found", status_code=404)

        return User(
            id=model.id,
            email=model.email,
            name=model.name
        )


    async def find_all(self, skip: int = 0, limit: int = 10) -> List[User]:
        statement = (
            select(UserModel)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(statement)
        models = result.scalars().all()
        
        return [
            User(id=m.id, name=m.name, email=m.email)
            for m in models
        ]


    async def update_user(self, user_id: int, name: str, email: str) -> User:
        model = await self.session.get(UserModel, user_id)
        if not model:
            raise HTTPException(detail="User not found", status_code=404)

        model.name = name
        model.email = email

        await self.session.flush()

        return User(
            id=model.id,
            email=model.email,
            name=model.name
        )



    async def delete_user(self, user_id: int) -> bool:
        model = await self.session.get(UserModel, user_id)
        if not model:
            return False

        await self.session.delete(model)
        self.session.flush()

        return True
    

    async def find_by_email_or_name(self, name: str, email: str, offset: int = 0, limit: int = 10) -> List[User] | List:
        statement = select(UserModel).offset(offset).limit(limit).where(
            or_(
                UserModel.name.ilike(f"%{name}%"),
                UserModel.email.ilike(f"%{email}%")
            )
        )

        result = await self.session.execute(statement)
        models = result.scalars().all()

        return [
            User(id=m.id, name=m.name, email=m.email)
            for m in models
        ]



    async def get_count_all_user(self) -> int:
        statement = select(func.count()).select_from(UserModel)

        result = await self.session.execute(statement)

        return result.scalar_one()



    async def find_by_email_and_name(self, name: str, email: str, offset: int = 0, limit: int = 10) -> List[User] | List:
        statement = select(UserModel).offset(offset).limit(limit).where(
            and_(
                UserModel.name.ilike(f"%{name}%"),
                UserModel.email.ilike(f"%{email}%")
            )
        )

        result = await self.session.execute(statement)
        models = result.scalars().all()

        return [
            User(id=m.id, name=m.name, email=m.email)
            for m in models
        ]
        

    
