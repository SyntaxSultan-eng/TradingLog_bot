from data.database import async_session
from data.database import Deal
#from sqlalchemy import select
from datetime import datetime
import aiofiles
import json
# import asyncio


async def check_names(message: str) -> bool:
    async with aiofiles.open(r"data\requirements\data.json", "r", encoding="utf-8") as file:
        data = json.loads(await file.read())
    
    if message.upper() in data.values() or message.upper() in data.keys():
        return True
    return False

async def add_new_stock(name : str, amount : int, price : float, deal_type : str):
    current_time = datetime.now()
    async with async_session() as session:
        new_deal = Deal(
            name_stock=name,
            type_of_deal = deal_type,
            amount_stock=amount,
            price_stock=price,
            date_deal=current_time 
        )
        session.add(new_deal)
        await session.commit()
        

# async def main():
#     result = await check_names("мЕЧеЛ")
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())

