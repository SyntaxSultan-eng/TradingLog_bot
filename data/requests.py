from data.database import async_session
from data.database import Stock
from sqlalchemy import select


async def add_name_stock(title: str):
    async with async_session() as session:
        stock = await session.scalar(select(Stock).where(Stock.name_stock == title))

        if not stock:
            session.add(Stock(name_stock = title))
            await session.commit()

