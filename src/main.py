import asyncio
from aiogram import Bot, Dispatcher

from config.config import config
from core.logger import logger, Logging_Middleware
from database.database import engine, init_db, health_check
from middleware.middleware import DB_Session_Middleware
from handlers.main_handlers import main_router


async def on_startup():
    """Действия при запуске бота"""
    try:
        await init_db()

        if await health_check():
            logger.info("Database connection established successfully")
        else:
            logger.critical("Failed to establish database connection")
            raise RuntimeError("Database connection failed")

    except Exception as e:
        logger.critical(f"Startup failed: {str(e)}", exc_info=True)
        raise

    logger.info("Bot started successfully")


async def on_shutdown():
    """Действия при остановке бота"""
    try:
        await engine.dispose()
        logger.info("Database engine disposed successfully")
    except Exception as e:
        logger.error(f"Error disposing database engine: {str(e)}", exc_info=True)

    logger.info("Bot stopped")


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
