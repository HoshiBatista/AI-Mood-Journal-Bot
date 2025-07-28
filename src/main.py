import asyncio
from aiogram import Bot, Dispatcher

from config.config import config
from core.logger import logger, Logging_Middleware
from database.database import on_startup, on_shutdown
from middleware.middleware import DB_Session_Middleware
from handlers.main_handlers import main_router


async def main():
    logger.info("Starting Mood Journal Bot initialization...")

    logging_middleware = Logging_Middleware(logger)
    db_middleware = DB_Session_Middleware()

    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(main_router)

    dp.update.outer_middleware(logging_middleware)
    dp.update.outer_middleware(db_middleware)

    logger.debug("Middlewares registered")

    logger.info("Starting bot polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user (Ctrl+C).")
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}", exc_info=True)
        raise
