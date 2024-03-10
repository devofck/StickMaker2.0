from aiogram.utils.keyboard import (InlineKeyboardMarkup,
                                    InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    ReplyKeyboardBuilder,
                                    ReplyKeyboardMarkup,
                                    KeyboardButton,
                                    )
from aiogram.types import ReplyKeyboardRemove

from config_reader import sticker_global_settings


def ask_create_pack():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='🚀 Создать первый набор',
            callback_data='create_first_pack'
        )
    )
    return kb.as_markup()


def main_user_menu():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text='💎 Управление наборами')
    ).row(
        KeyboardButton(text='⭕️ Жалоба на чужой набор')
    )
    return kb.as_markup(resize_keyboard=True)


def accept_or_decline_sticker_pack():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text='🚀 Оставляем', callback_data='continue_creating_pack'),
    ).add(
        InlineKeyboardButton(text='🧬 Хочу поменять', callback_data='set_another_title')
    )
    return kb.as_markup()


def explore_pack(link: str):
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text='👀 Посмотреть набор ',
            url=link
        ),
    ).row(
        InlineKeyboardButton(
            text='🟢 Добавить стикеры',
            callback_data='add_sticker_to_exists_pack:' + link.split('/')[-1]
        )
    )
    return kb.as_markup()


def pack_menu():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text='📚 Мои наборы', callback_data='my_packs')
    )
    return kb.as_markup()


def my_sets(sets):
    kb = InlineKeyboardBuilder()
    for pack in sets:
        kb.row(
            InlineKeyboardButton(
                text=pack.title.replace(sticker_global_settings.username, ''),
                callback_data=f'pack_menu:{pack.name}'
            )
        )
    kb.row(
        InlineKeyboardButton(text='🪄 Создать новый', callback_data='create_new_pack')
    )

    return kb.as_markup()


def pack_management(name):
    kb = InlineKeyboardBuilder()
    look_at_pack = InlineKeyboardButton(
        text='🔎 Посмотреть набор',
        url='https://t.me/addstickers/' + name
    )
    add_sticker = InlineKeyboardButton(
        text='🌴 Добавить стикер',
        callback_data=f'add_sticker_to_exists_pack:{name}'
    )
    delete_sticker = InlineKeyboardButton(
        text='🧨 Удалить стикер',
        callback_data=f'delete_sticker_from_exists_pack:{name}'
    )
    delete_pack = InlineKeyboardButton(
        text='💣 Удалить ВЕСЬ стикерпак',
        callback_data=f'delete_pack:{name}'
    )
    rename_pack = InlineKeyboardButton(
        text='✏️ Переименовать набор',
        callback_data=f'rename_exists_pack:{name}'
    )
    publish_pack = InlineKeyboardButton(
        text='🏖 Опубликовать оф канале бота',
        callback_data=f'publish_pack:{name}'
    )
    return kb.row(
        look_at_pack
    ).row(
        add_sticker,
        delete_sticker
    ).row(
        rename_pack
    ).row(
        publish_pack
    ).as_markup()


def back_to_sticker_management(name):
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='🔙 Назад в меню',
            callback_data=f'pack_menu:{name}'
        )
    )
    return kb.as_markup()


def back_to_sticker_management_rk():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(
            text='🔙 Назад в меню'
        )
    )
    return kb.as_markup(resize_keyboard=True)


def remove_keyboard_buttons():
    kb = ReplyKeyboardRemove()
    return kb


def back_to_main_menu():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data='back_to_main_menu'
        )
    )
    return kb.as_markup()


def can_i_help():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='Да, помоги мне!',
            callback_data="accept_report_help_order"
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='Нет, спасибо!',
            callback_data='deny_report_help_order'
        )
    )
    return kb.as_markup()


def ask_for_reason_of_report():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='Он оскорбляет честь и достоинстово',
            callback_data='reason:0',
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='Он демонстрирует насилие',
            callback_data='reason:1'
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='Набор содержит 18+ контент',
            callback_data='reason:2'
        )
    )
    return kb.as_markup()


def verdict(name):
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='Посмотреть набор',
            url='https://t.me/addstickers/' + name
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='🗑 Удалить набор',
            callback_data='delete_pack:' + name
        ),
        InlineKeyboardButton(
            text='✅ Сохранить набор',
            callback_data='keep_pack:' + name
        )
    )
    return kb.as_markup()


def look_pack(name):
    kb = InlineKeyboardBuilder()
    look_at_pack = InlineKeyboardButton(
        text='🔎 Посмотреть набор',
        url='https://t.me/addstickers/' + name
    )
    kb.add(look_at_pack)
    return kb.as_markup()


def start_btn():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text="/start")
    )
    return kb.as_markup(resize_keyboard=True)


def motiv_kb(channels):
    kb = InlineKeyboardBuilder()

    for channel in channels:
        kb.row(
            InlineKeyboardButton(
                text=channel.title,
                url=channel.link
            )
        )
    kb.row(
        InlineKeyboardButton(
            text='✅ Я подписался',
            callback_data='check_sub'
        )
    )
    return kb.as_markup()
