import asyncio
from dispatcher import dp, bot
from handlers import auth_router

async def main():
    dp.include_router(auth_router)
    print("bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())