import os

from states.user.pack_management_states import AddStickers
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types import Message, InputSticker
from funcs.sticker_sets.name_generator import random_file_name, get_random_emojis
from funcs.sticker_sets.formatter import get_converted_file

stickers_add = Router()


@stickers_add.message(AddStickers.add_stickers, F.sticker.is_video)
async def add_video_sticker_to_set(m: Message, state: FSMContext, bot: Bot):
    file = await bot.get_file(file_id=m.sticker.file_id)
    destination_directory = random_file_name('.webm')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    data = await state.get_data()
    await bot.add_sticker_to_set(
        user_id=m.from_user.id,
        name=data['name'],
        sticker=InputSticker(
            sticker=FSInputFile(
                path=destination_directory
            ),
            emoji_list=[m.sticker.emoji]
        )
    )
    await m.answer("<b>✅ Стикер добавлен в набор!</b>")
    os.remove(destination_directory)


@stickers_add.message(AddStickers.add_stickers, F.photo)
async def add_photo_to_set(m: Message, state: FSMContext, bot: Bot):
    file = await bot.get_file(file_id=m.photo[-1].file_id)
    destination_directory = random_file_name('.jpg')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    data = await state.get_data()
    new_file = get_converted_file(
        source_file=destination_directory
    )
    await bot.add_sticker_to_set(
        user_id=m.from_user.id,
        name=data['name'],
        sticker=InputSticker(
            sticker=FSInputFile(
                path=new_file
            ),
            emoji_list=get_random_emojis()
        )
    )
    await m.answer("<b>✅ Стикер добавлен в набор!</b>")
    os.remove(new_file)


@stickers_add.message(AddStickers.add_stickers, F.sticker.is_animated == False)
async def add_photo_sticker_to_set(m: Message, state: FSMContext, bot: Bot):
    file = await bot.get_file(file_id=m.sticker.file_id)
    destination_directory = random_file_name('.png')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    data = await state.get_data()
    new_file = get_converted_file(
        source_file=destination_directory
    )
    await bot.add_sticker_to_set(
        user_id=m.from_user.id,
        name=data['name'],
        sticker=InputSticker(
            sticker=FSInputFile(
                path=new_file
            ),
            emoji_list=[m.sticker.emoji]
        )
    )
    await m.answer("<b>✅ Стикер добавлен в набор!</b>")
    os.remove(new_file)


@stickers_add.message(AddStickers.add_stickers, F.video_note)
async def add_video_note_to_set(m: Message, state: FSMContext, bot: Bot):
    file = await bot.get_file(file_id=m.video_note.file_id)
    destination_directory = random_file_name('.mp4')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    data = await state.get_data()
    new_file = get_converted_file(
        source_file=destination_directory
    )
    await bot.add_sticker_to_set(
        user_id=m.from_user.id,
        name=data['name'],
        sticker=InputSticker(
            sticker=FSInputFile(
                path=new_file
            ),
            emoji_list=get_random_emojis()
        )
    )
    await m.answer("<b>✅ Стикер добавлен в набор!</b>")
    os.remove(new_file)


@stickers_add.message(AddStickers.add_stickers, F.video)
async def add_video_to_set(m: Message, state: FSMContext, bot: Bot):
    if m.video.duration > 15:
        await m.answer(
            '<b>Видео слишком длинное!</b>'
        )
        return
    file = await bot.get_file(file_id=m.video.file_id)
    destination_directory = random_file_name('.mp4')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    data = await state.get_data()
    new_file = get_converted_file(
        source_file=destination_directory
    )
    await bot.add_sticker_to_set(
        user_id=m.from_user.id,
        name=data['name'],
        sticker=InputSticker(
            sticker=FSInputFile(
                path=new_file
            ),
            emoji_list=get_random_emojis()
        )
    )
    await m.answer("<b>✅ Стикер добавлен в набор!</b>")
    os.remove(new_file)
