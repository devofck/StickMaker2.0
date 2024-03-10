from aiogram.fsm.state import State, StatesGroup


class RenamePack(StatesGroup):
    waiting_for_name = State()
    confirm_name = State()


class AddStickers(StatesGroup):
    add_stickers = State()


class DeleteStickers(StatesGroup):
    delete_stickers = State()


class Reports(StatesGroup):
    wait_for_sticker = State()


class PackCreation(StatesGroup):
    wait_for_name = State()
    wait_for_sticker = State()


class BlockUntilStarted(StatesGroup):
    block = State()
