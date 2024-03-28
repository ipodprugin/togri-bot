import os
import aiofiles

from settings.config import settings


async def download_item(session, path: str, filename: str):
    params = {'path': path}
    url = 'https://cloud-api.yandex.net/v1/disk/resources/download'
    download_link  = None

    async with session.get(url, params=params) as response:
        if response.status != 200:
            return None
        resp = await response.json()
        download_link = resp.get('href')

    if not os.path.isdir('img'):
        os.mkdir('img')
    zippath = f'{settings.IMGS_PATH}/{filename}.zip'
    async with session.get(download_link) as resp:
        # with open(zippath, 'wb') as fd:
        async with aiofiles.open(zippath, 'wb') as fd:
            async for chunk in resp.content.iter_chunked(1024):
                await fd.write(chunk)
            await fd.flush()
    return zippath


async def find_plan_img(images) -> list[int]:
    ids = []
    for index, img in enumerate(images):
        if img.find('План этажа') != -1:
            ids.append(index)
    return ids


async def find_facade_img(images):
    for index, img in enumerate(images):
        if img.find('Общий фасад здания.jpg') != -1:
            return index
    return None
