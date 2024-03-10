"""
Legends never die
Отче, сохрани его от падение и прочих несчастий
Аминь
"""

import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
import handlers.private as private_funcs
from handlers.channel.channel_requests_processor import requests
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from session import session
from database.models import Base
from middlewares.session_factory import DbSessionMiddleware
from handlers.private.admin.admin_panel import admin_panel
from handlers.special.leave_manager import leave_manager


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
        leave_manager,
        private_funcs.start_router,
        requests,
        private_funcs.stick_processor,
        private_funcs.main_user_menu,
        private_funcs.stickers_add,
        admin_panel
    )
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
