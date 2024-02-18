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
    AddStickers,
    DeleteStickers,
    Reports
)
from funcs.sticker_sets.report_builder import build_report
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


@main_user_menu.callback_query(F.data.startswith('delete_sticker_from_exists_pack'))
async def delete_stickers(c: CallbackQuery, state: FSMContext, bot: Bot):
    name = c.data.split(':')[1]
    await state.set_state(DeleteStickers.delete_stickers)
    await state.update_data(
        name=name
    )
    await c.message.delete()
    last_msg = await c.message.answer(
        '<b>Отправляйте стикеры из ЭТОГО набора, чтобы его удалить!</b>',
        reply_markup=keyboard.back_to_sticker_management(name)
    )
    await state.update_data(
        last_msg=last_msg.message_id
    )


@main_user_menu.message(F.sticker, DeleteStickers.delete_stickers)
async def delete_sent_sticker_from_pack(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = data['name']
    try:
        await bot.delete_message(
            chat_id=m.from_user.id,
            message_id=data['last_msg']
        )
    except Exception as ex:
        print(ex)
    if m.sticker.set_name != name:  # skip stickers from another sets
        last_msg = await m.answer(
            '<b>❌ Вы отправили стикер НЕ из этого набора!</b>',
            reply_markup=keyboard.back_to_sticker_management(name=name)
        )
        await state.update_data(
            last_msg=last_msg.message_id
        )
    elif m.sticker.set_name == name:
        await bot.delete_sticker_from_set(
            sticker=m.sticker.file_id
        )
        last_msg = await m.answer(
            '<b>✅ Стикер успешно удален из набора!</b>',
            reply_markup=keyboard.back_to_sticker_management(name)
        )
        await state.update_data(
            last_msg=last_msg.message_id
        )
    else:
        await m.delete()


@main_user_menu.message(F.text == '⭕️ Жалоба на чужой набор')
async def send_report(m: Message, state: FSMContext):
    await m.answer(
        text='<b>🚨 Отправить жалобу на набор</b>\n'
        '<i>Жалобы абсолютно анонимны, нарушитель не узнает о вас</i>\n\n'
        'Если вы считаете, что кто-то создал набор стикеров, нарушаюший законодательство '
        'Российской Федерации или Республики Беларусь (либо набор просто может нанести кому-либо вред), то '
        'отправьте жалобу на набор и мы его удалим!\n\n'
        '<b>Отправить жалобу легко - просто пришлите любой стикер из набора!\n\n'
        '</b>',
        reply_markup=keyboard.back_to_main_menu()
    )
    await state.set_state(Reports.wait_for_sticker)


@main_user_menu.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(c: CallbackQuery, state: FSMContext):
    await state.clear()
    await c.message.edit_text(
        text='✅ Вы успешно вернулись в главное меню!',
    )


@main_user_menu.message(F.sticker.set_name.endswith(sticker_global_settings.bot_postfix), Reports.wait_for_sticker)
async def send_report(m: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await m.answer(
        '<b>✅ Жалоба на набор успешно отправлена!</b>\n\n'
        'Мы сообщим вам о результатах проверки'
    )
    await bot.send_message(
        chat_id=sticker_global_settings.reports_id,
        text='<b>Жалоба на набор!</b>\n\n',
        reply_markup=keyboard.verdict(m.sticker.set_name)
    )


@main_user_menu.message(F.sticker, Reports.wait_for_sticker)
async def miss_sticker_sent_for_report(m: Message, state: FSMContext):
    await m.answer(
        '<b>Данный стикерпак создан НЕ через нашего бота..</b>\n\n'
        'Увы, но удалить данный набор не в наших силах..\n\n'
        'Хотите, мы поможем вам составить жалобу, а вы ее отправите на sticker@telegram.org ?\n'
        '(На данную почту модерация телеграм принимает жалобы на стикерпаки)',
        reply_markup=keyboard.can_i_help()
    )
    await state.update_data(set_name=m.sticker.set_name)


@main_user_menu.callback_query(F.data == 'deny_report_help_order')
async def deny_report_help_order(c: CallbackQuery):
    await c.message.edit_text(
        'Ок! Если что, ты знаешь к кому обращаться 😉'
    )


@main_user_menu.callback_query(F.data == 'accept_report_help_order')
async def accept_report_help_order(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(
        'В связи с чем вы хотите подать жалобу на набор?',
        reply_markup=keyboard.ask_for_reason_of_report()
    )


@main_user_menu.callback_query(F.data.startswith('reason'))
async def return_report_text(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    out_text = build_report(int(c.data.split(':')[1]), data['set_name'])
    await state.clear()
    await c.message.edit_text(
        f"<code>{out_text}</code>"
    )
    await c.message.answer(
        '✅ Отправьте жалобу с этим текстом на официальную почту: sticker@telegram.org\n'
        '<i>Разумеется, вы можете редактировать этот текст под конкретный случай</i>'
    )
