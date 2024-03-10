from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from typing import Union


async def is_subscribed(bot: Bot, user: Union[Message, CallbackQuery], channel_id: Union[int, str]) -> bool:
    """
    :param bot: aiogram bot instance
    :param user: message or callback object
    :param channel_id: channel id (int or str)
    :return: True if person  subscribed
    """
    user_id = user.from_user.id
    status = (await bot.get_chat_member(
        chat_id=channel_id,
        user_id=user_id
    )).status
    if status == 'left' or status == 'banned':
        return False
    else:
        return True
