from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import async_sessionmaker
from sqlalchemy.pool import NullPool

from config.config import config
from core.logger import logger
from models.models import Base

engine = create_async_engine(
    config.postgres_url,
    echo=False,
    future=True,
    poolclass=NullPool,
    connect_args={
        "command_timeout": 30,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def init_db():
    """Инициализация базы данных (создание таблиц)"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.critical(f"Database initialization failed: {str(e)}", exc_info=True)
        raise


async def health_check():
    """Проверка работоспособности подключения к БД"""
    try:
        async with engine.connect() as conn:
            result = await conn.scalar("SELECT 1")
            if result == 1:
                logger.debug("Database health check: OK")
                return True
        return False
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}", exc_info=True)
        return False
