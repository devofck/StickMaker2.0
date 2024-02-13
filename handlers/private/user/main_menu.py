import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from handlers.private.user import keyboard
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models import User, StickerPack
from sqlalchemy import select, update
from config_reader import sticker_global_settings
from states.user.pack_management_states import (
    RenamePack,
    AddStickers
)
from funcs.sticker_sets.title_generation import format_title

main_user_menu = Router()


@main_user_menu.message(F.text == '💎 Управление наборами')
async def show_my_packs(m: Message, session: AsyncSession):
    sets = await session.scalars(
        select(
            StickerPack
        ).where(
            StickerPack.owner_id == m.from_user.id
        )
    )
    await m.answer(
        text='<b>🤩 Вот список ваших наборов!</b>\n\n'
             'Кликни на нужный для взаимодействия',
        reply_markup=keyboard.my_sets(sets)
    )


@main_user_menu.callback_query(F.data.startswith('pack_menu'))
async def pack_menu(c: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()
    pack_name = c.data.split(':')[1]
    pack: StickerPack = await session.scalar(
        select(StickerPack).where(StickerPack.name == pack_name)
    )
    pack_tg = await bot.get_sticker_set(
        name=pack_name
    )
    await c.message.edit_text(
        f'<b>🔥 Набор "{pack.title.replace(sticker_global_settings.username, "")}"</b>\n'
        f'<i>Стикеров в наборе: {len(pack_tg.stickers)}</i>\n\n'
        f'<b>⚒ Воспользуйтесь клавиатурой ниже для управления своим набором</b>',
        reply_markup=keyboard.pack_management(pack_name)
    )


# ------------- RENAME PACK -------------> START POINT
@main_user_menu.callback_query(F.data.startswith('rename_exists_pack'))
async def rename_pack(c: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(RenamePack.waiting_for_name)
    name = c.data.split(':')[1]
    pack = await bot.get_sticker_set(
        name=name
    )
    await c.message.edit_text(
        '<b>Введите новое название для набора</b>\n\n'
        f'P.S текущее название набора: {pack.title.replace(sticker_global_settings.username, "")}',
        reply_markup=keyboard.back_to_sticker_management(name)
    )
    await state.update_data(
        name=name
    )


@main_user_menu.message(F.text, RenamePack.waiting_for_name)
async def getting_new_pack_name(m: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if len(m.text) > 20:
        await m.answer('<b>Упс.. название слишком длинное!</b>\n\n'
                       'Попробуйте еще раз :)')
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
        RenamePack.confirm_name
    )

    await state.update_data(
        pack_title=format_title(m.text, sticker_global_settings.username)
    )


@main_user_menu.callback_query(F.data == 'continue_creating_pack', RenamePack.confirm_name)
async def accept_changing_pack_title(c: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    data = await state.get_data()
    name = data['name']
    pack_title = data['pack_title']
    await bot.set_sticker_set_title(
        name=name,
        title=pack_title
    )
    await session.execute(
        update(StickerPack).where(StickerPack.name == name).values(title=pack_title)
    )
    await session.commit()
    await c.message.edit_text(
        '<b>Название успешно обновлено!</b>',
        reply_markup=keyboard.back_to_sticker_management(name)
    )


@main_user_menu.callback_query(F.data == 'set_another_title', RenamePack.confirm_name)
async def set_another_title(c: CallbackQuery, state: FSMContext):
    try:
        await c.message.delete()
    except:
        pass
    data = await state.get_data()
    name = data['name']
    await c.message.answer(
        '<b>Честно говоря, название мне тоже не понравилось 😁))\n\n</b>'
        'Введи новое название для набора!',
        reply_markup=keyboard.back_to_sticker_management(name)
    )
    await state.set_state(
        RenamePack.waiting_for_name
    )


@main_user_menu.message(F.text == '🔙 Назад в меню', AddStickers.add_stickers)
async def back_to_menu_rk(m: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await m.answer(
        '<b>✅ Пополнение стикеров окончено!</b>',
        reply_markup=keyboard.remove_keyboard_buttons()
    )
    data = await state.get_data()
    pack_name = data['name']
    await state.clear()
    pack: StickerPack = await session.scalar(
        select(StickerPack).where(StickerPack.name == pack_name)
    )
    pack_tg = await bot.get_sticker_set(
        name=pack_name
    )
    await m.answer(
        f'<b>🔥 Набор "{pack.title.replace(sticker_global_settings.username, "")}"</b>\n'
        f'<i>Стикеров в наборе: {len(pack_tg.stickers)}</i>\n\n'
        f'<b>⚒ Воспользуйтесь клавиатурой ниже для управления своим набором</b>',
        reply_markup=keyboard.pack_management(pack_name)
    )


@main_user_menu.callback_query(F.data.startswith('add_sticker_to_exists_pack'))
async def add_stickers_to_pack(c: CallbackQuery, state: FSMContext):
    name = c.data.split(":")[1]
    await c.message.delete()
    await c.message.answer(
        text="<b>Ну.. пришел час творить 👩‍🎨!</b>\n\n"
             "Отправляйте фото/стикеры/гифки и даже видео!\n"
             "Все это я добавлю в твой стикерпак!\n\n"
             "⭕️ Чтобы прекратить добавление стикеров, нажмите на кнопку под клавиатурой",
        reply_markup=keyboard.back_to_sticker_management_rk()
    )
    await state.set_state(AddStickers.add_stickers)
    await state.update_data(
        name=name
    )
