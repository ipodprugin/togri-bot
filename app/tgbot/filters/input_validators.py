from aiogram.filters import BaseFilter
from aiogram.types import Message

from .. import config


class ValidTenderIdInput(BaseFilter):
    async def __call__(self, message: Message):
        lines = message.text.split('\n') 
        if len(lines) > 5:
            await message.reply('Я пока не могу обработать за раз такой объём информации. Введите не больше 5 значений')
            return False
        # for line in lines:
        #     if not config.TENDER_ID_REGEX.findall(line):
        #         return False
        return True
