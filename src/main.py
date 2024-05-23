import logging
import asyncio

from settings.bot_config import bot, dp
from handlers.driver import driver_router
from handlers.group import group_router
from handlers.user import user_router


async def main():
    dp.include_routers(user_router, group_router, driver_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
