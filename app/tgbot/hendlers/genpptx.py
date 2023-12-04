import os
import shutil
import aiohttp
import pygsheets
import zipfile

from pathlib import Path

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from settings.config import settings
from services.gsheets.data import get_data
from services.yadisk.images import find_facade_img, find_plan_img, download_item
from services.gen_pptx.render import render_pptx

from ..filters.input_validators import ValidTenderIdInput

from .helpers import chunker

router = Router()


async def form_pictures_dict(imgs_folder: str):
    # TODO: Перенести в более подходящее место
    pictures = settings.PICTURES_PLACEHOLDERS.copy()
    images = os.listdir(imgs_folder)

    plan_img_index = await find_plan_img(images)
    if plan_img_index is not None:
        pictures['plan'] = f'{imgs_folder}/{images[plan_img_index]}'
        images.pop(plan_img_index)

    facade_img_index = await find_facade_img(images)
    if facade_img_index is not None:
        pictures['map'] = f'{imgs_folder}/{images[facade_img_index]}'
        images.pop(facade_img_index)

    for index, img in enumerate(images):
        if index == 9:
            break
        pictures[f'Img{index + 1}'] = f'{imgs_folder}/{img}'
    
    return pictures


@router.message(Command("pptx"))
async def cmd_start(message: Message):
    await message.reply(
        f'Таблица: {settings.GSHEETURL}\n\nВведите tender_id объектов, для которых необходимо сгенерировать презентацию (каждый на новой строке).'
    )


@router.message(
    F.text,
    ValidTenderIdInput()
)
async def gen_pptx_handler(message: Message):
    botmessage = await message.answer("Собираю данные...")
    print('connecting to GSheets...')
    sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    print('Opening gsheet by url...')
    sh = sa.open_by_url(settings.GSHEETURL)

    tenders = message.text.split('\n')

    for _tenders in chunker(tenders, 5):
        print(f'Getting data for {_tenders}')
        _tenders = await get_data(
            gsheet=sh,
            search_data=_tenders,
            worksheet_title='Помещения (копия)'
        )

        await botmessage.edit_text("Скачиваю фотографии с Я.Диска 🌆")
        print('downloading images from yadisk...')

        basepath = 'app:/nonresidential/'
        DISK_AUTH_HEADERS: str = {'accept': 'application/json', 'Authorization': 'OAuth %s' % settings.YADISK_OAUTH_TOKEN}
        async with aiohttp.ClientSession(headers=DISK_AUTH_HEADERS) as session:
            for tender in _tenders:
                zippath = await download_item(session=session, path=basepath + tender.id, filename=tender.id)
                tender.imgzippath = zippath

        await botmessage.edit_text(f"Распаковываю скачанное 📦")
        print('unpacking images from yadisk zip files...')

        for tender in _tenders:
            with zipfile.ZipFile(tender.imgzippath, "r") as zip_ref:
                zip_ref.extractall(settings.IMGS_PATH)

        await botmessage.edit_text(f"Генерирую презентации 🤖")

        tenders_count = len(_tenders)
        generated_pptx_paths = []
        for index, tender in enumerate(_tenders):

            progress_bar = f"{(index + 1) * '🟩'}{(tenders_count - index + 1) * '⬛️'}"
            await botmessage.edit_text(f"Генерирую презентации для: {tender.id} 🤖\n\n{progress_bar}")
            print('generating pptx for tender: %s...' % tender.id)

            imgs_folder, _ = os.path.splitext(tender.imgzippath)
            print(f'----- {tender = }, {imgs_folder = }')
            pictures = await form_pictures_dict(imgs_folder)
            print(f'----- {pictures = }')
            generated_pptx_paths.append(await render_pptx(tender=tender, pictures=pictures))

        await botmessage.edit_text(f'Финальные штрихи. Ещё немного...')

        for tender in _tenders:
            print('deleting zip and its unpacked files: %s...' % tender.imgzippath)
            imgs_folder, _ = os.path.splitext(tender.imgzippath)
            shutil.rmtree(imgs_folder)
            os.remove(tender.imgzippath)
        
        for path in generated_pptx_paths:
            await message.reply_document(
                document=FSInputFile(path),
                caption=Path(path).stem
            )
            os.remove(path)
        
    await botmessage.delete()
        # for path in generated_pptx_paths:
        