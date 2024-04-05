import aiohttp
from settings.config import settings
from services.data.models import SheetRowTenderContent


async def get_data_from_db(
    search_data: list,
):
    _by = 'address'
    if settings.TENDER_ID_REGEX.findall(search_data[0]):
        _by = 'tender_id'

    async with aiohttp.ClientSession() as session:
        params = {'params': search_data, 'by': _by}
        async with session.get(f'{settings.PARSER_API_URL}/tenders', params=params) as response:
            if response.status == 200:
                tenders = await response.json()
                print(f'\n-------------\n{tenders = }\n')
                for index, tender in enumerate(tenders):
                    tenders[index] = SheetRowTenderContent.model_validate(tender)
                print(f'\n-------------\n{tenders = }\n')
                return tenders

