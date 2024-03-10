from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from database.models import Channel


def admin_menu():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text='📊 Статистика',
            callback_data='get_stat'
        ),
        InlineKeyboardButton(
            text='🤩 Мотив',
            callback_data='motiv_settings'
        )
    )
    return kb.as_markup()


def motiv_management():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='➕ Добавить',
            callback_data='add_channel'
        ),
        InlineKeyboardButton(
            text='➖ Удалить',
            callback_data='delete_channel'
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_admin'
        )
    )
    return kb.as_markup()


def accept_channel():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text='✅ Одобрить',
            callback_data='accept_channel'
        ),
        InlineKeyboardButton(
            text='❌ Отклонить',
            callback_data='decline_channel'
        )
    )
    kb.row(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_admin'
        )
    )
    return kb.as_markup()


def channels_to_delete(channels):
    kb = InlineKeyboardBuilder()

    for channel in channels:
        kb.row(
            InlineKeyboardButton(
                text=f'{channel.title}',
                callback_data=f'delete_current_channel:{channel.channel_id}'
            )
        )
    kb.row(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_admin'
        )
    )
    return kb.as_markup()


def back_to_admin_panel():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_admin'
        )
    )
    return kb.as_markup()
