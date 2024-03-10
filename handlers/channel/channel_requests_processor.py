from aiogram import Router, Bot
from aiogram.types.input_file import FSInputFile
from aiogram.types import ChatJoinRequest
from aiogram.fsm.context import FSMContext
from handlers.private.user.keyboard import start_btn
from sqlalchemy.ext.asyncio.session import AsyncSession
from states.user.pack_management_states import BlockUntilStarted
from sqlalchemy import select
from database.models import User
requests = Router()


@requests.chat_join_request()
async def process_join_request(req: ChatJoinRequest, bot: Bot, state: FSMContext, session: AsyncSession):
    user = await session.scalar(
        select(User).where(User.id == req.from_user.id)
    )
    if not user:
        await bot.send_photo(
            chat_id=req.from_user.id,
            photo=FSInputFile(
                path='static/join_ad/join_ad.jpg',
            ),
            caption='<b>⌛️ Создай свой стикерпак за 30 секунд!</b>\n\n'
                    'Жми на кнопку ниже и мы взлетаем 🚀\n\n'
                    '<b>upd:</b> т к от тебя пришла заявка в канал, то весь функционал доступен бесплатно '
                    'и навсегда!',
            reply_markup=start_btn()
        )
        await state.set_state(BlockUntilStarted.block)
        return
    await bot.send_message(
        chat_id=req.from_user.id,
        text='<b>🤩 Ух ты! Теперь ты еще в нашем каталоге!</b>\n\n'
             'Очень приятно тебя тут видеть) надеюсь, что-нибудь найдешь для себя'
    )
