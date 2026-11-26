from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundException
from src.modules.products.entity import Product
from src.modules.products.model import ProductModel
from sqlalchemy import select, or_, and_, func
from typing import List

from src.modules.products.schema import ProductUpdate

class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: Product) -> Product:
        model = ProductModel(
            name = product.name,
            price = product.price
        )

        self.session.add(model)
        self.session.flush()

        return Product(
            id=model.id,
            name=model.name,
            price=model.price
        )



    async def find_all(self, offset: int = 0, limit: int = 10) -> List[Product]:
        statment = (
            select(ProductModel)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(statment)
        models = result.scalars().all()

        return [
            Product(id=m.id, name=m.name, price=m.price)
            for m in models
        ]
    

    async def get_by_id(self, id: int):
        statment = (
            select(ProductModel)
            .where(ProductModel.id == id)
        )

        result = await self.session.execute(statment)
        model  = result.scalar_one_or_none()

        if not model:
            raise NotFoundException

        
        return Product(
            id=model.id,
            name=model.name,
            price=model.price
        )

    async def get_by_name(self, name: str) -> List[Product]:
        statment = (
            select(ProductModel)
            .where(
                ProductModel.name.ilike(f"%{name}%")
            )
        )

        result = await self.session.execute(statment)

        models = result.scalars().all()

        return [
            Product(id=m.id, name=m.name, price=m.price)
            for m in models
        ]


    async def delete(self, id: int) -> bool:
        statement = (
            select(ProductModel)
            .where(ProductModel.id == id)
        )

        result = await self.session.execute(statement)
        model  = result.scalar_one_or_none()

        if not model:
            raise NotFoundException

        await self.session.delete(model)
        self.session.flus()

        return True

    async def update(self, id: int, product: ProductUpdate) -> Product:
        statement = (
            select(ProductModel)
            .where(ProductModel.id == id)
        )

        result = await self.session.execute(statement)
        model  = result.scalar_one_or_none()

        if not model:
            raise NotFoundException

        model.name = product.name
        model.price = product.price

        await self.session.flush()

        return Product(
            id=model.id,
            name=model.name,
            price=model.price
        )

