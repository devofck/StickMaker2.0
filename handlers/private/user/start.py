import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from handlers.private.user import keyboard
from aiogram.fsm.context import FSMContext
from states.user.first_pack_state import FirstPack
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models import User
from sqlalchemy import select
from states.user.pack_management_states import BlockUntilStarted
from funcs.sticker_sets.title_generation import format_title
from config_reader import sticker_global_settings
from filters.chat_type_filter import ChatTypeFilter

start_router = Router()
start_router.message.filter(
    ChatTypeFilter(
        chat_type='private'
    )
)

@start_router.message(CommandStart())
async def start_bot(m: Message, state: FSMContext, session: AsyncSession):
    user = await session.scalar(
        select(User.status).where(User.id == m.from_user.id)
    )
    if user == 0:
        # if user already has been registered
        await m.answer(
            '<b>👋 И тебе бип-боп-привет!</b>\n\n'
            'Воспользуйся меню ниже!',
            reply_markup=keyboard.main_user_menu()
        )
        await state.clear()
    elif not user:
        # if it is new user
        new_user = User(
            id=m.from_user.id,
            status=0
        )
        session.add(new_user)
        await session.commit()
        await m.answer_sticker(
            sticker='CAACAgIAAxkBAAEXE-NlNugrdm07DGm'
                    'duPJ0i7HB82I7TgACxDcAAqLd0Eq1HDHLy7P_ETAE',
            reply_markup=keyboard.remove_keyboard_buttons()
        )
        await asyncio.sleep(1)
        await m.answer(
            'Привет! Я <b>Стик Мейкер</b>! Давай знакомиться!'
        )
        await asyncio.sleep(2)
        await m.answer(
            '😊 <b>Я помогу тебе создать стикерпак в пару кликов!</b>\n\n'
            'Создай набор и просто кидай мне чужие '
            '<b>стикеры</b>, <b>гифки</b>, <b>фото</b> '
            'и даже <b>видео</b>!\n\n'
            'Все это будет добавлено в набор! 😏'
        )
        await asyncio.sleep(4)
        await m.answer(
            '😉 Попробуем?',
            reply_markup=keyboard.ask_create_pack()
        )


@start_router.message(BlockUntilStarted.block)
async def block_until_started(m: Message, state: FSMContext):
    await m.answer(
        '<b>☝️ Для корректного начала работы, отправьте боту /start !</b>\n\n'
        'Ну или просто по приколу кнопкой ниже)))',
        reply_markup=keyboard.start_btn()
    )


@start_router.callback_query(F.data == 'create_first_pack')
async def create_first_pack(c: CallbackQuery, state: FSMContext):
    try:
        await c.message.delete()
    except:
        pass
    await c.message.answer_sticker(
        'CAACAgIAAxkBAAEXE-VlNuhw5qXCqTs'
        'SgY1ok-H-KMNJuAACpzYAApAj2UpiLSo-Wk3OFDAE'
    )
    await asyncio.sleep(1)
    await c.message.answer_photo(
        caption="Супер! <b>Введи название для будущего набора</b>\n\n"
                "Хорошенько подумай, ведь <b>его увидят все, "
                "кто захочет воспользоваться набором!</b>!",
        photo=FSInputFile(
            path='static/manual/title_location.jpg'
        )
    )
    await state.set_state(
        FirstPack.enter_name
    )


@start_router.message(FirstPack.enter_name)
async def check_name(m: Message, state: FSMContext):
    if len(m.text) > 20:
        await m.answer('<b>Упс.. название слишком длинное!</b>\n\n' + 'Попробуйте еще раз :)')
        return
    text = (f'😌 Неплохо.. вы назвали свой набор <b>"{m.text}"</b>\n\n'
            f'Оставляем такое название или меняем?')

    if 'флип' in m.text.lower() or 'fleep' in m.text.lower():
        text += ('\n\nБатюшки.. <a href="https://t.me/fleepy4">Флип</a> - это '
                 'мой создатель..')
    await m.answer(
        text,
        reply_markup=keyboard.accept_or_decline_sticker_pack()
    )
    await state.set_state(
        FirstPack.confirm_name
    )

    await state.update_data(
        pack_title=format_title(m.text, sticker_global_settings.username)
    )


@start_router.callback_query(FirstPack.confirm_name, F.data == 'set_another_title')
async def decline_pack_title(c: CallbackQuery, state: FSMContext):
    try:
        await c.message.delete()
    except:
        pass
    await c.message.answer(
        '<b>Честно говоря, название мне тоже не понравилось 😁))\n\n</b>'
        'Введи новое название для набора!'
    )
    await state.set_state(
        FirstPack.enter_name
    )


@start_router.callback_query(FirstPack.confirm_name)
async def approve_pack_title(c: CallbackQuery, state: FSMContext):
    try:
        await c.message.delete()
    except:
        pass
    data = await state.get_data()
    await c.message.answer(
        f"<b>{data['pack_title'].replace(sticker_global_settings.username, '')}</b> - звучит сильно 🤘!\n"
        f"<i>🚀 У набора есть будущее!</i>\n\n"
        f"Пришли стикер, фотку, GIF или даже видео и я помещу его в набор!"
    )
    await state.set_state(
        FirstPack.enter_first_sticker
    )
