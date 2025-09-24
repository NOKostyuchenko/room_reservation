from sqlalchemy import Integer, Column
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import settings


class PreBase:


    @declared_attr
    def __tablename__(cls):
        #  Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()
    

    #  Во все таблицы будет добавлено поле ID
    id = Column(Integer, primary_key=True)


#  В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

#  Asynchronous session generator function for dependency injection
async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session

