from typing import Union
from sqlalchemy.ext.asyncio.session import AsyncSession
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database.models import User
from sqlalchemy import select
from aiogram import Bot
from sqlalchemy import select
from database.models import Channel
from typing import Union
from funcs.motiv.subscribe_checker import is_subscribed
from handlers.private.user.keyboard import motiv_kb


class IsSubscribed(BaseFilter):
    async def __call__(self, req: Union[Message, CallbackQuery], session: AsyncSession, bot: Bot) -> bool:
        channels = await session.scalars(
            select(Channel)
        )
        for channel in channels:
            if not await is_subscribed(bot=bot, user=req, channel_id=channel.channel_id):
                channels = await session.scalars(
                    select(Channel)
                )
                await bot.send_message(
                    chat_id=req.from_user.id,
                    text='Для пользования ботом подпишитесь на канал! Это бесплатно :)',
                    reply_markup=motiv_kb(channels)
                )
                return False
        return True
