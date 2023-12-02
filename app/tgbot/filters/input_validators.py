from aiogram.filters import BaseFilter
from aiogram.types import Message

from .. import config


class ValidTenderIdInput(BaseFilter):
    async def __call__(self, message: Message):
        for line in message.text.split('\n'):
            if not config.TENDER_ID_REGEX.findall(line):
                return False
        return True
