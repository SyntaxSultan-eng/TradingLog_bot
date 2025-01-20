import asyncio
from decouple import config
from aiogram import Bot, Dispatcher

#####################################

API_TOKEN = config("BOT_API_KEY",default = '')
bot = Bot(API_TOKEN)
dp = Dispatcher()

#####################################

async def on_startup() -> None:
    print("Bot has started working🚀", end = '\n\n')

async def main() -> None:
    dp.startup.register(callback = on_startup)
    await dp.start_polling(bot)

############################################

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot has stopped working❌')