import asyncio
import json
from aiogram import Bot, Dispatcher
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi!")
