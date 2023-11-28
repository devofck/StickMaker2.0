from aiogram.utils.keyboard import (InlineKeyboardMarkup,
                                    InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    ReplyKeyboardBuilder,
                                    ReplyKeyboardMarkup,
                                    KeyboardButton)


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
        KeyboardButton(text='💎 Создать набор')
    ).add(
        KeyboardButton(text='📕 Инструкция')
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
            callback_data='add_sticker_to:' + link.split('/')[-1]
        )
    )
    return kb.as_markup()
