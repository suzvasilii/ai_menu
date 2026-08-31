import asyncio
from dispatcher import dp, bot
from handlers import orders_router, auth_router

async def main():
    dp.include_router(orders_router)
    dp.include_router(auth_router)
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())