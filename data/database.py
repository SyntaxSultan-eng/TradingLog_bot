from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String,Numeric,DateTime
from datetime import datetime

engine = create_async_engine(url='sqlite+aiosqlite:///StocksInfo.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs,DeclarativeBase):
    pass


class Deal(Base):
    __tablename__ = "Deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_stock: Mapped[str] = mapped_column(String(70))
    ticker: Mapped[str] = mapped_column(String(5))
    type_of_deal: Mapped[str] = mapped_column(String(7), index = True)
    amount_stock: Mapped[int] = mapped_column()
    price_stock: Mapped[float] = mapped_column(Numeric(10, 2))
    full_price_stock: Mapped[float] = mapped_column(Numeric(10,2))
    date_deal : Mapped[datetime] = mapped_column(DateTime)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
