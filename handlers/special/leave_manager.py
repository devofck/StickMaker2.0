from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated, Message
from aiogram import F, Router
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import update
from database.models import User
leave_manager = Router()
leave_manager.my_chat_member.filter(F.chat.type == "private")
leave_manager.message.filter(F.chat.type == "private")


@leave_manager.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    await session.execute(
        update(User).where(User.id == event.from_user.id).values(status=2)
    )
    await session.commit()


@leave_manager.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    await session.execute(
        update(User).where(User.id == event.from_user.id).values(status=0)
    )
    await session.commit()
