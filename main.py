import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions, base_interface

async def main():
    bot = Bot(token="7130470880:AAEeQk2CVU4xDAxCop7nyLs14lzlkVohf2U")
    dp = Dispatcher()
    dp.include_routers(base_interface.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
