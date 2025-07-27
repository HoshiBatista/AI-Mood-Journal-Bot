import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config.config import config
from core.logger import logger, Logging_Middleware
from database.database import engine, init_db, health_check
from middleware.middleware import DB_Session_Middleware


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


bot = Bot(token=config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    logger.info(
        f"User {user.id} started bot", extra={"user": f"{user.id} ({user.username})"}
    )

    welcome_text = (
        f"✨ Привет, {user.full_name}!\n\n"
        "🌱 Я твой персональный помощник для отслеживания настроения и эмоций VibeScribe.\n\n"
        "Со мной ты сможешь:\n"
        "• 📝 Вести дневник настроения\n"
        "• 📊 Анализировать эмоциональные паттерны\n"
        "• 🔮 Получать прогнозы настроения\n"
        "• 📤 Формировать отчеты для психолога\n\n"
        "Начни с команды /new_entry чтобы добавить первую запись!\n"
        "Или используй /help для списка команд."
    )

    await message.answer(welcome_text)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "🌟 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/new_entry - Добавить новую запись о настроении\n"
        "/stats - Показать статистику настроений\n"
        "/report - Создать отчет\n"
        "/predict - Прогноз настроения\n"
        "/settings - Настройки профиля\n"
        "/help - Показать это сообщение"
    )
    await message.answer(help_text)


@dp.message(Command("new_entry"))
async def new_entry_command(message: types.Message):
    logger.info(f"User {message.from_user.id} started new entry")
    await message.answer(
        "📝 Давайте создадим новую запись!\n"
        "Оцените свое настроение по шкале от 1 до 5, где:\n"
        "1 - Очень плохое 😔\n"
        "2 - Плохое 😞\n"
        "3 - Нормальное 😐\n"
        "4 - Хорошее 😊\n"
        "5 - Отличное 😄"
    )


async def main():
    logger.info("Starting Mood Journal Bot initialization...")

    logging_middleware = Logging_Middleware()
    db_middleware = DB_Session_Middleware()

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
