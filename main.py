import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
import handlers.private as private_funcs
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from session import session
from database.models import Base
from middlewares.session_factory import DbSessionMiddleware

async def main() -> None:
    """
    point of entry
    """
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        disable_web_page_preview=True,
        parse_mode='HTML',
        session=session
    )
    engine = create_async_engine(
        url=f'postgresql+asyncpg://'
            f'{config.PG_USER}:'
            f'{config.password}@'
            f'{config.ip}:'
            f'{config.port}/'
            f'{config.base}',
        echo=True,
        future=True
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    storage = RedisStorage(
        Redis()
    )
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        private_funcs.start_router,
        private_funcs.stick_processor
    )
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
