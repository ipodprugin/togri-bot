import logging
import shutil, os

from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from settings.config import settings

from .hendlers import genpptx


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TGTOKEN.get_secret_value())

dp = Dispatcher()
dp.include_routers(
    genpptx.router,
)


def clean_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
clean_folder(settings.PPTX_OUTPUT_DIRPATH)
clean_folder(settings.IMGS_PATH)
