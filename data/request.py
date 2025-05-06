from data.database import async_session
from data.database import Deal
from sqlalchemy import select,func
from datetime import datetime
import aiofiles
import json
import os

import asyncio


async def check_names(message: str) -> bool:
    async with aiofiles.open(os.path.join('data','requirements','forpdf.json'), "r", encoding="utf-8") as file:
        data = json.loads(await file.read())
    
    if message.lower() in [name.lower() for name in data.values()] or message.upper() in data.keys():
        return True
    return False

async def get_full_info(TickerOrName : str) -> dict:
    async with aiofiles.open(os.path.join('data','requirements','data.json'), "r", encoding="utf-8") as file:
        data = json.loads(await file.read())

    async with aiofiles.open(os.path.join('data','requirements','stocks_price.json'), "r", encoding="utf-8") as file:
        prices = json.loads(await file.read())

    TickerOrName = TickerOrName.upper()

    for stock in data:
        if TickerOrName in [i.upper() for i in list(stock.values())[:2] ]:
            return stock, prices


async def add_new_stock(name : str, amount : int, price : float, deal_type : str):
    current_time = datetime.now()
    stock, prices = await get_full_info(name)

    async with async_session() as session:
        new_deal = Deal(
            name_stock=stock["Название компании"],
            full_name = stock["Полное название"],
            ticker = stock["Тикер"],
            lotsize = stock["Размер лота"],
            price_for1_stock = prices[stock["Тикер"]],
            isin = stock["ISIN"],
            type_of_deal = deal_type,
            amount_lots=amount,
            price_stock=price,
            current_price = prices[stock["Тикер"]]*stock["Размер лота"]*amount,
            date_deal=current_time 
        )
        session.add(new_deal)
        await session.commit()

async def full_info() -> dict:
    async with async_session() as session:
        info_state ={
            'total_deals' : await session.scalar(select(func.count(Deal.id))), #Общее количество совершенных сделок.
            'total_deals_buy' : await session.scalar(select(func.count(Deal.id)).where(Deal.type_of_deal == "Покупка")),
            'total_deals_sell' : await session.scalar(select(func.count(Deal.id))) - 
            await session.scalar(select(func.count(Deal.id)).where(Deal.type_of_deal == "Покупка")),
            'total_buy' : await session.scalar(select(func.sum(Deal.price_stock)).where(Deal.type_of_deal == "Покупка")) or 0, # Вся сумма покупки.
            'total_sell' : await session.scalar(select(func.sum(Deal.price_stock)).where(Deal.type_of_deal == "Продажа")) or 0, # Вся сумма продаж.     
        }
        #.scalar - лучше подходит для возврата числа или строки, а .execute - для множества данных. Func.count подсчитывает кол-во строк с данным параметром.
        #func.sum считает сумму всех ячеек с условием "Покупка"/"Продажа". Мы можем не беспокоиться о TypeError, потому что проверка проходит в handlers.

    return info_state

async def main():
    result = await get_full_info("posi")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

