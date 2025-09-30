from typing import Optional, TypeVar, Generic, Type, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):


    def __init__(self, model: Type[ModelType]):
        self.model = model


    #  Get an object by id
    async def get(
            self,
            object_id: int,
            session: AsyncSession
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()


    #  Get all objects of the specified class
    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        db_object = await session.scalars(select(self.model))
        return db_object.all()


    #  Create a new object
    async def create(
            self,
            object_in: CreateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        object_in_data: dict = object_in.model_dump()
        db_object = self.model(**object_in_data)
        
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)

        return db_object
    

    #  Update an object
    async def update(
            self,
            db_object: ModelType,
            object_in: CreateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        db_obj_data = jsonable_encoder(db_object)
        update_data = object_in.model_dump(exclude_unset=True)

        for field in db_obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        
        return db_object
    

    #  Delete an object
    async def delete(
            self,
            db_object: int,
            session: AsyncSession
    ) -> ModelType:
        await session.delete(db_object)
        await session.commit()

        return db_object

