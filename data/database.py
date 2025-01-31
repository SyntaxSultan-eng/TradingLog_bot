from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String

engine = create_async_engine(url='sqlite+aiosqlite:///StocksInfo.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs,DeclarativeBase):
    pass


class Stock(Base):
    __tablename__ = "Deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_stock: Mapped[str] = mapped_column(String(30))



async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
