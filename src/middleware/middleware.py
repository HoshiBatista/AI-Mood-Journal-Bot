from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Any, Dict

from database.database import Async_Session_Local
from core.logger import logger


class DB_Session_Middleware(BaseMiddleware):
    """Middleware для инъекции сессии БД в обработчики"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with Async_Session_Local() as session:
            data["session"] = session
            logger.debug("Database session created for request")

            try:
                result = await handler(event, data)

                await session.commit()
                logger.debug("Database transaction committed")

                return result

            except Exception as e:
                await session.rollback()
                logger.error(
                    f"Database transaction rolled back due to error: {str(e)}",
                    exc_info=True,
                )
                raise
            finally:
                await session.close()
                logger.debug("Database session closed")
