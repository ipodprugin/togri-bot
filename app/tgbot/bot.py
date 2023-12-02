import logging

from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from app.settings.config import settings

from app.tgbot.hendlers import genpptx


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TGTOKEN.get_secret_value())

dp = Dispatcher()
dp.include_routers(
    genpptx.router,
)
