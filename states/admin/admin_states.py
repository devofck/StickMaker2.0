from aiogram.fsm.state import State, StatesGroup


class Motiv(StatesGroup):
    wait_for_link = State()
    wait_for_channel_info = State()
    wait_for_accept = State()
