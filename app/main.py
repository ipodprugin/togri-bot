import asyncio
import uvicorn

from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI

from settings.config import settings
from tgbot.bot import bot, dp


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.delete_webhook(drop_pending_updates=True)
    webhook_info = await bot.get_webhook_info()

    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(url=settings.WEBHOOK_URL)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(settings.WEBHOOK_ENDPOINT)
async def bot_webhook(update: dict):
    print('--- update, ---\n', update)
    tgupdate = types.Update(**update)
    await dp._process_update(bot=bot, update=tgupdate)


async def run_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if settings.DEBUG:
        asyncio.run(run_polling())
    else:
        uvicorn.run(
            'main:app', 
            host=settings.HOST, 
            port=settings.PORT
        )