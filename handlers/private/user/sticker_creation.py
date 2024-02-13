import asyncio
import os
import time

from aiogram.types import Message
from aiogram import Router, F, Bot
from states.user.first_pack_state import FirstPack
from aiogram.fsm.context import FSMContext
from funcs.sticker_sets.name_generator import create_uniq_name, random_file_name, get_random_emojis
from aiogram.types import InputSticker
from aiogram.types import FSInputFile
from handlers.private.user.keyboard import explore_pack, main_user_menu
from funcs.sticker_sets.formatter import get_converted_file
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models import StickerPack, User

stick_processor = Router()


async def gratitude_for_first_creation(tg_id: int, link: str, bot: Bot):
    await bot.send_message(
        chat_id=tg_id,
        text='❤️ Пуфф! <b>Это твой первый набор!\n\nМои поздравления</b> или как радуются'
        ' боты вроде меня:\n"🎉 БИП-БУП БИМ-БИМ!!!"',
        reply_markup=explore_pack(link)
    )
    await bot.send_message(
        chat_id=tg_id,
        text='<b>🙃 Кстати! Ты прошел мини обучения по боту!</b>\n'
             '<i>Да.. все было так просто</i>\n\n'
             'Как быстро они растут 😢',
        reply_markup=main_user_menu()
    )


# create first_sticker
@stick_processor.message(FirstPack.enter_first_sticker, F.sticker.is_video)
async def process_first_video_sticker(m: Message, state: FSMContext, bot: Bot, session: AsyncSession):
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
    new_set = StickerPack(
        name=name,
        owner_id=m.from_user.id,
        title=data['pack_title'],
        date=int(time.time()),
    )
    session.add(new_set)
    await session.commit()
    os.remove(destination_directory)
    link = 'https://t.me/addstickers/' + name

    await state.clear()
    await gratitude_for_first_creation(m.from_user.id, link, bot)


@stick_processor.message(FirstPack.enter_first_sticker, F.photo)
async def process_first_photo(m: Message, state: FSMContext, bot: Bot, session: AsyncSession):
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
    new_set = StickerPack(
        name=name,
        owner_id=m.from_user.id,
        title=data['pack_title'],
        date=int(time.time()),
    )
    session.add(new_set)
    await session.commit()
    link = 'https://t.me/addstickers/' + name
    os.remove(new_file)
    await state.clear()
    await gratitude_for_first_creation(m.from_user.id, link, bot)
    os.remove(new_file)


@stick_processor.message(FirstPack.enter_first_sticker, F.video_note)
async def process_first_photo(m: Message, state: FSMContext, bot: Bot, session: AsyncSession):
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
    new_set = StickerPack(
        name=name,
        owner_id=m.from_user.id,
        title=data['pack_title'],
        date=int(time.time()),
    )
    session.add(new_set)
    await session.commit()

    link = 'https://t.me/addstickers/' + name
    os.remove(new_file)
    await state.clear()
    await gratitude_for_first_creation(m.from_user.id, link, bot)


@stick_processor.message(FirstPack.enter_first_sticker, F.sticker.is_animated == False)
async def process_photo_sticker(m: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    data = await state.get_data()
    name = create_uniq_name()
    file = await bot.get_file(
        m.sticker.file_id
    )
    file_title = random_file_name('.png')
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
            emoji_list=[m.sticker.emoji]
        )]
    )
    new_set = StickerPack(
        name=name,
        owner_id=m.from_user.id,
        title=data['pack_title'],
        date=int(time.time()),
    )
    session.add(new_set)
    await session.commit()
    link = 'https://t.me/addstickers/' + name
    os.remove(new_file)
    await state.clear()
    await gratitude_for_first_creation(m.from_user.id, link, bot)


@stick_processor.message(FirstPack.enter_first_sticker, F.video)
async def process_video(m: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    if m.video.duration > 15:
        await m.answer(
            '<b>Видео слишком длинное!</b>'
        )
    data = await state.get_data()
    name = create_uniq_name()
    file = await bot.get_file(file_id=m.video.file_id)
    destination_directory = random_file_name('.mp4')
    await bot.download_file(
        file_path=file.file_path,
        destination=destination_directory
    )
    new_file = get_converted_file(destination_directory)

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
    new_set = StickerPack(
        name=name,
        owner_id=m.from_user.id,
        title=data['pack_title'],
        date=int(time.time()),
    )
    session.add(new_set)
    await session.commit()

    link = 'https://t.me/addstickers/' + name
    os.remove(new_file)
    await state.clear()
    await gratitude_for_first_creation(m.from_user.id, link, bot)
