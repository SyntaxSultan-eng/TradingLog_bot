# from data.database import async_session
# from data.database import Stock
# from sqlalchemy import select
import aiofiles
import json
# import asyncio


async def check_names(message: str) -> bool:
    async with aiofiles.open(r"data\requirements\data.json", "r", encoding="utf-8") as file:
        data = json.loads(await file.read())
    
    if message.upper() in data.values() or message.upper() in data.keys():
        return True
    return False

async def add_new_stock():
    pass
    #async with async_session() as session:


# async def main():
#     result = await check_names("мЕЧеЛ")
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())

