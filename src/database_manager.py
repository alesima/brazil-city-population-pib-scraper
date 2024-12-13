import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base, Municipio

lock = asyncio.Lock()


class DatabaseManager:
    def __init__(self, db_url='sqlite+aiosqlite:///municipios.db'):
        self.engine = create_async_engine(
            db_url, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)

    async def initialize(self):
        async with self.engine.connect() as conn:
            await conn.execute(text("PRAGMA journal_mode = WAL"))
            await conn.run_sync(Base.metadata.create_all)

    async def add_city(self, city: Municipio):
        async with lock, self.Session() as session, session.begin():
            try:
                session.add(city)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise RuntimeError(
                    f"Failed to add city to database: {e}") from e

    async def get_all_cities(self):
        async with self.engine.begin() as conn:
            result = await conn.execute(select(Municipio))
            return result.scalars().all()

    async def get_city_by_id(self, id: int):
        async with lock, self.engine.begin() as conn:
            result = await conn.execute(
                select(Municipio).filter(Municipio.id == id)
            )
            return result.scalar_one_or_none()

    async def close(self):
        await self.engine.dispose()
