import asyncio
import logging

from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from data.handlers import router
from data.database import create_db

#####################################

API_TOKEN = config("BOT_API_KEY",default = '')
bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

#####################################

async def on_startup() -> None:
    print("Bot has started working🚀", end = '\n\n')

async def main() -> None:
    await create_db()
    dp.startup.register(callback = on_startup)
    dp.include_router(router=router)
    await dp.start_polling(bot)

############################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot has stopped working❌')