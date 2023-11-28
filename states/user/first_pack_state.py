from aiogram.fsm.state import State, StatesGroup


class FirstPack(StatesGroup):
    enter_name = State()
    confirm_name = State()
    enter_first_sticker = State()
