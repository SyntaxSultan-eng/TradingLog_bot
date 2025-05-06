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
    full_name: Mapped[str] = mapped_column(String(120))
    ticker: Mapped[str] = mapped_column(String(5))
    lotsize: Mapped[int] = mapped_column()
    isin: Mapped[str] = mapped_column(String(20))
    type_of_deal: Mapped[str] = mapped_column(String(7), index = True)
    amount_lots: Mapped[int] = mapped_column()
    price_for1_stock : Mapped[float] = mapped_column(Numeric(10,2))
    price_stock: Mapped[float] = mapped_column(Numeric(10, 2))
    current_price: Mapped[float] = mapped_column(Numeric(20, 2))
    date_deal : Mapped[datetime] = mapped_column(DateTime)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
