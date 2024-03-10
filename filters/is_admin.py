from typing import Union
from sqlalchemy.ext.asyncio.session import AsyncSession
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database.models import User
from sqlalchemy import select
from typing import Union


class IsAdmin(BaseFilter):
    async def __call__(self, req: Union[Message, CallbackQuery], session: AsyncSession) -> bool:
        status = await session.scalar(
            select(User.status).where(User.id == req.from_user.id)
        )
        return status == 1
