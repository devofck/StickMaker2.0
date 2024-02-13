from aiogram.fsm.state import State, StatesGroup


class RenamePack(StatesGroup):
    waiting_for_name = State()
    confirm_name = State()


class AddStickers(StatesGroup):
    add_stickers = State()
