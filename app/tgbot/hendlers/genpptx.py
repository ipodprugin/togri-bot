import os
import shutil
import aiohttp
import pygsheets
import zipfile
import pprint

from pathlib import Path

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, FSInputFile

from settings.config import settings
from services.data.gsheets import get_data
from services.data.from_db import get_data_from_db
from services.data.models import SheetRowTenderContent
from services.yadisk.images import find_facade_img, find_plan_img, download_item
from services.gen_pptx.render import render_pptx

from ..filters.input_validators import ValidTenderIdInput

# from .helpers import chunker

router = Router()

pp = pprint.PrettyPrinter(indent=4)

async def form_pictures_dict(imgs_folder: str):
    # TODO: Перенести в более подходящее место
    pictures = settings.PICTURES_PLACEHOLDERS.copy()
    images = os.listdir(imgs_folder)

    plan_imgs_indexes = await find_plan_img(images)
    if plan_imgs_indexes is not None:
        pictures['plan'] = f'{imgs_folder}/{images[plan_imgs_indexes[0]]}'
        images = [img for i, img in enumerate(images) if i not in plan_imgs_indexes]

    # Добавление фасада отменено в template3 шаблоне
    # facade_img_index = await find_facade_img(images)
    # if facade_img_index is not None:
    #     pictures['map'] = f'{imgs_folder}/{images[facade_img_index]}'
    #     images.pop(facade_img_index)

    for index, img in enumerate(images, start=1):
        if index == 13:
            break
        pictures[f'Img{index}'] = f'{imgs_folder}/{img}'
    
    return pictures


@router.message(Command("pptx"))
async def cmd_start(
    message: Message,
    command: CommandObject
):
    print(command.args)
    await message.reply(
        f'Таблица: {settings.GSHEETURL}\n\nВведите tender_id объектов, для которых необходимо сгенерировать презентацию (каждый на новой строке).'
    )


@router.message(
    F.text,
    ValidTenderIdInput() # TODO: Добавить регулярку на адрес
)
async def gen_pptx_handler(message: Message):
    botmessage = await message.answer("Собираю данные...")

    params = message.text.split('\n')
    print(f'Getting data for {params}')
    _tenders = await get_data_from_db(params)
    if not _tenders:
        await botmessage.edit_text("Я не нашёл таких тендеров 🤷")
        return

    await botmessage.edit_text("Скачиваю фотографии с Я.Диска 🌆")
    print('downloading images from yadisk...')

    DISK_AUTH_HEADERS = {'accept': 'application/json', 'Authorization': 'OAuth %s' % settings.YADISK_OAUTH_TOKEN}
    async with aiohttp.ClientSession(headers=DISK_AUTH_HEADERS) as session:
        for tender in _tenders:
            zippath = await download_item(session=session, path=tender.imgzippath, filename=tender.tender_id)
            tender.imgzippath = zippath

    await botmessage.edit_text(f"Распаковываю скачанное 📦")
    print('unpacking images from yadisk zip files...')

    for tender in _tenders:
        _imgs_folder = f'{settings.IMGS_PATH}/{tender.tender_id}/'
        with zipfile.ZipFile(tender.imgzippath, "r") as zf:
            for index, info in enumerate(zf.infolist()):
                outname = info.filename
                if outname.endswith('.jpg'):
                    plan_imgs_indexes = await find_plan_img([outname])
                    info.filename = 'План этажа.jpg' if plan_imgs_indexes else f'{index}.jpg'
                    zf.extract(info, path=_imgs_folder)

    await botmessage.edit_text(f"Генерирую презентации 🤖")

    tenders_count = len(_tenders)
    generated_pptx_paths = []
    for index, tender in enumerate(_tenders):

        progress_bar = f"{(index + 1) * '✅'}{(tenders_count - index - 1) * '🕐'}"
        await botmessage.edit_text(f"Генерирую презентации для: {tender.tender_id} 🤖\n\n{progress_bar}")
        print('generating pptx for tender: %s...' % tender.tender_id)

        imgs_folder, _ = os.path.splitext(tender.imgzippath)
        pictures = await form_pictures_dict(imgs_folder)
        generated_pptx_paths.append(await render_pptx(tender=tender, pictures=pictures))

    await botmessage.edit_text(f'Финальные штрихи. Ещё немного...')

    for path in generated_pptx_paths:
        await message.reply_document(
            document=FSInputFile(path),
            caption=Path(path).stem
        )
        os.remove(path)

    for tender in _tenders:
        print('deleting zip and its unpacked files: %s...' % tender.imgzippath)
        imgs_folder, _ = os.path.splitext(tender.imgzippath)
        shutil.rmtree(imgs_folder)
        os.remove(tender.imgzippath)

    await botmessage.delete()

