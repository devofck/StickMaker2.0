import asyncio
import os

from aiogram.types import Message
from aiogram import Router, F, Bot
from states.user.first_pack_state import FirstPack
from aiogram.fsm.context import FSMContext
from funcs.sticker_sets.name_generator import create_uniq_name, random_file_name, get_random_emojis
from aiogram.types import InputSticker
from aiogram.types import FSInputFile
from handlers.private.user.keyboard import explore_pack
from funcs.sticker_sets.formatter import get_converted_file
stick_processor = Router()


# create first_sticker
@stick_processor.message(FirstPack.enter_first_sticker, F.sticker.is_video)
async def process_first_video_sticker(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = create_uniq_name()
    file = await bot.get_file(file_id=m.sticker.file_id)
    destination_directory = random_file_name('.webm')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    await bot.create_new_sticker_set(
        user_id=m.from_user.id,
        name=name,
        title=data['pack_title'],
        sticker_format='video',
        stickers=[InputSticker(
            sticker=FSInputFile(
                path=destination_directory,
            ),
            emoji_list=[m.sticker.emoji]
        )]
    )
    os.remove(destination_directory)
    link = 'https://t.me/addstickers/' + name

    await state.clear()
    await m.answer(
        '❤️ Пуфф! <b>Это твой первый набор!\n\nМои поздравления</b> или как радуются'
        ' боты вроде меня:\n"🎉 БИП-БУП БИМ-БИМ!!!"',
        reply_markup=explore_pack(link)
    )


@stick_processor.message(FirstPack.enter_first_sticker, F.photo)
async def process_first_photo(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = create_uniq_name()
    file = await bot.get_file(
        m.photo[-1].file_id
    )
    file_title = random_file_name('.jpg')
    await bot.download_file(
        file_path=file.file_path,
        destination=file_title
    )
    await m.answer(
        str(get_random_emojis())
    )
    new_file = get_converted_file(file_title)
    await bot.create_new_sticker_set(
        user_id=m.from_user.id,
        name=name,
        title=data['pack_title'],
        sticker_format='video',
        stickers=[InputSticker(
            sticker=FSInputFile(
                path=new_file,
            ),
            emoji_list=get_random_emojis()
        )]
    )

    link = 'https://t.me/addstickers/' + name
    # os.remove(new_file)
    await state.clear()
    await m.answer(
        '❤️ Пуфф! <b>Это твой первый набор!\n\nМои поздравления</b> или как радуются'
        ' боты вроде меня:\n"🎉 БИП-БУП БИМ-БИМ!!!"',
        reply_markup=explore_pack(link)
    )


@stick_processor.message(FirstPack.enter_first_sticker, F.video_note)
async def process_first_photo(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = create_uniq_name()
    file = await bot.get_file(
        m.video_note.file_id
    )
    file_title = random_file_name('.mp4')
    await bot.download_file(
        file_path=file.file_path,
        destination=file_title
    )

    new_file = get_converted_file(file_title, content_type='video_note')
    await m.answer(
        str(get_random_emojis()) + '\n' + new_file
    )
    await bot.create_new_sticker_set(
        user_id=m.from_user.id,
        name=name,
        title=data['pack_title'],
        sticker_format='video',
        stickers=[InputSticker(
            sticker=FSInputFile(
                path=new_file,
            ),
            emoji_list=get_random_emojis()
        )]
    )

    link = 'https://t.me/addstickers/' + name
    # os.remove(new_file)
    await state.clear()
    await m.answer(
        '❤️ Пуфф! <b>Это твой первый набор!\n\nМои поздравления</b> или как радуются'
        ' боты вроде меня:\n"🎉 БИП-БУП БИМ-БИМ!!!"',
        reply_markup=explore_pack(link)
    )