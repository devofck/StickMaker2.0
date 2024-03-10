import time

import aiogram.exceptions
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func, delete
from database.models import User, StickerPack, Channel
from states.admin.admin_states import Motiv
import handlers.private.admin.keyboard as keyboard

from filters.is_admin import IsAdmin
from aiogram.types.input_file import FSInputFile
from funcs.admin.stat_graph import draw_graph
import datetime
import psutil

admin_panel = Router()

admin_panel.message.filter(IsAdmin())
admin_panel.callback_query.filter(IsAdmin())


@admin_panel.message(Command('admin'))
async def admin_auth(m: Message, state: FSMContext, session: AsyncSession):
    await m.answer(
        '<b>Вы успешно вошли в панель администратора!</b>',
        reply_markup=keyboard.admin_menu()
    )


@admin_panel.callback_query(F.data == 'get_stat')
async def load_stat(c: CallbackQuery, session: AsyncSession, bot: Bot):
    total_users = await session.scalar(
        select(func.count(User.id))
    )
    users_alive = await session.scalar(
        select(
            func.count(
                User.id
            ).filter(
                User.status != 2
            )
        )
    )
    sticker_sets = await session.scalar(
        select(
            func.count(StickerPack.name)
        )
    )
    today = datetime.datetime(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day
    )
    today_users = await session.scalar(
        select(
            func.count(
                User.id
            ).filter(
                User.date >= today
            )
        )
    )
    await c.message.delete()

    draw_graph(users_alive, sticker_sets)
    time_1 = time.time()
    await c.message.answer_photo(
        photo=FSInputFile(
            path='stats.png',

        ),
        caption='<b>📈 Статистика</b>\n\n'
                '👤 Информация о пользователях:\n'
                f'🙄 Всего людей: {total_users}\n'
                f'🥳 Живых люжей: {users_alive}\n'
                f'☠️ Мертвых людей: {total_users - users_alive}\n\n'
                f'💎 Информация о стикерпаках\n'
                f'👏 Количество наборов: {sticker_sets}\n\n'
                f'🤖 Свободные ресурсы машины:\n'
                f'ОЗУ: {str(100 - psutil.virtual_memory().percent) + "%"}\n'
                f'ЦП: {str(100 - psutil.cpu_percent(interval=1)) + "%"}',
        reply_markup=keyboard.back_to_admin_panel()
    )


@admin_panel.callback_query(F.data == 'motiv_settings')
async def motiv_settings(c: CallbackQuery, state: FSMContext, session: AsyncSession):
    channels = await session.scalars(
        select(Channel)
    )
    channels_humanized = ''
    for channel in channels:
        channels_humanized += f'<b>{channel.title}</b>: {channel.subs} переходов!\n'

    if channels_humanized == '':
        await c.message.edit_text(
            '<b>Каналы в мотиве отсутствуют!</b>',
            reply_markup=keyboard.motiv_management()
        )
    else:
        channels_humanized = "<b>📈 Каналы в мотиве:</b>\n" + channels_humanized
        await c.message.edit_text(
            channels_humanized,
            reply_markup=keyboard.motiv_management()
        )


@admin_panel.callback_query(F.data == 'add_channel')
async def add_channel(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(
        '<b>Отправьте ссылку на канал!</b>',
        reply_markup=keyboard.back_to_admin_panel()
    )
    await state.set_state(Motiv.wait_for_link)


@admin_panel.message(F.text.startswith("https://"), Motiv.wait_for_link)
async def process_link(m: Message, state: FSMContext):
    await state.update_data(
        link=m.text
    )
    await m.answer(
        '<b>Отправьте пост с канала, либо же ID канала!</b>'
    )
    await state.set_state(Motiv.wait_for_channel_info)


@admin_panel.message(F.forward_from_chat, Motiv.wait_for_channel_info)
async def parse_id_from_forwarded_post(m: Message, state: FSMContext):
    await state.update_data(
        channel_id=m.forward_from_chat.id
    )
    data = await state.get_data()
    await m.answer(
        f'<b>Мотив готов к установке!</b>\n\n'
        f'ID канала: {m.forward_from_chat.id}\n'
        f'Ссылка на канал: {data["link"]}',
        reply_markup=keyboard.accept_channel()
    )
    await state.set_state(Motiv.wait_for_accept)


@admin_panel.message(F.text.startswith("-"), Motiv.wait_for_channel_info)
async def enter_id(m: Message, state: FSMContext):
    await state.update_data(
        channel_id=m.text
    )
    data = await state.get_data()
    await m.answer(
        f'<b>Мотив готов к установке!</b>\n\n'
        f'ID канала: {m.text}\n'
        f'Ссылка на канал: {data["link"]}',
        reply_markup=keyboard.accept_channel()
    )
    await state.set_state(Motiv.wait_for_link)


@admin_panel.callback_query(F.data == 'accept_channel', Motiv.wait_for_accept)
async def accept_channel(c: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    try:
        channel_data = await bot.get_chat(chat_id=data['channel_id'])
    except aiogram.exceptions.TelegramForbiddenError:
        await c.message.edit_text(
            '<b>Бот не является админом этого канала!</b>'
        )
        await state.clear()
        return

    channel = Channel()
    channel.title = channel_data.title
    channel.channel_id = channel_data.id
    channel.link = data['link']
    channel.subs = 0
    session.add(channel)
    await session.commit()
    await c.message.edit_text(
        '<b>Вы успешно добавили канал в мотив!</b>'
    )
    await state.clear()


@admin_panel.callback_query(F.data == 'decline_channel', Motiv.wait_for_link)
async def decline_channel(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(
        '<b>Вы отказались добавлять канал в мотив!</b>'
    )
    await state.clear()


@admin_panel.callback_query(F.data == 'delete_channel')
async def delete_channel(c: CallbackQuery, state: FSMContext, session: AsyncSession):
    channels = await session.scalars(
        select(Channel)
    )
    await c.message.edit_text(
        '<b>Список каналов, которые вы можете удалить</b>',
        reply_markup=keyboard.channels_to_delete(channels)
    )


@admin_panel.callback_query(F.data.startswith('delete_current_channel'))
async def delete_current_channel(c: CallbackQuery, session: AsyncSession):
    await session.execute(
        delete(Channel).where(Channel.channel_id == int(c.data.split(':')[1]))
    )
    await session.commit()
    channels = await session.scalars(
        select(Channel)
    )
    await c.message.edit_reply_markup(
        reply_markup=keyboard.channels_to_delete(channels)
    )


@admin_panel.callback_query(F.data == 'back_to_admin')
async def back_to_admin_panel(c: CallbackQuery, state: FSMContext):
    await state.clear()
    if c.message.photo:
        await c.message.delete()
        await c.message.answer(
            '<b>Вы успешно вошли в панель администратора!</b>',
            reply_markup=keyboard.admin_menu()
        )
        return
    await c.message.edit_text(
        '<b>Вы успешно вошли в панель администратора!</b>',
        reply_markup=keyboard.admin_menu()
    )
    