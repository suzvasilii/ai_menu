import asyncio
from dispatcher import dp, bot
from handlers import auth_router, orders_router

async def main():
    dp.include_router(auth_router)
    dp.include_router(orders_router)
    print("bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())