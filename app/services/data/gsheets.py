import pygsheets

from .models import SheetRowTenderContent
from settings.config import settings


async def _get_gsheet_row_by_cell_value(
    worksheet: pygsheets.Worksheet,
    cell_value: str, 
) -> SheetRowTenderContent | None:
    cell = worksheet.find(cell_value)
    if cell:
        row_id = cell[0].row
        row = worksheet.get_row(row_id)
        try:
            m1_start_price = row[-12]
            start_price = row[6]
            min_price = row[-6]
            object_area = row[-10]

            m1_start_price = '{:0.2f}'.format(float(m1_start_price)) if m1_start_price else None
            start_price = '{:0.2f}'.format(float(start_price)) if start_price else None
            min_price = float(min_price) if min_price else None
            object_area = float(object_area) if object_area else None

            m1_min_price = "{:.2f}".format(min_price / object_area) if min_price and object_area else None
            row = SheetRowTenderContent(
                id=row[1],
                address=row[2],
                region_name=row[3],
                district_name=row[4],
                object_area=object_area,
                floor=row[8],
                applications_enddate=row[10],
                deposit=row[7],
                start_price=start_price,
                m1_start_price=m1_start_price,
                procedure_form=settings.PROCEDURE_FORMS[row[5]],
                auction_step=row[-8],
                price_decrease_step=row[-7],
                min_price=min_price,
                m1_min_price=m1_min_price,
                tendering=row[-5],
                lat=row[-4],
                lon=row[-3],
            )
            print('-------- ROW', row)
            return row
        except IndexError as e:
            print(f'При обработке строки с {cell_value} произошла ошибка: {e}')
# ['', '19408694', 'ЮВАО, район Печатники, проезд Проектируемый 5112, вл. 10, этаж 1, помещение 3Н, комнаты 30-42, 44, 45', 'ЮВАО', 'Не определен', 'Открытый аукцион в электронной форме', '1606740', '321348', 'Не указано', 'нет', '15.01.2024', 'https://investmoscow.ru/tenders/tender/19408694', '', '', '', '40523.07692307692', '3213480.0', '79.3', 'Не указано', '80337.0', '0.0', '0.0', '', '', '', '', '']

async def get_gsheet_row_by_cell_value(
    gsheet: pygsheets.Spreadsheet, 
    cell_value: str, 
    worksheet_title: str | None = None
) -> SheetRowTenderContent | None:
    row = None
    if worksheet_title is None:
        worksheets = gsheet.worksheets()
        for w in worksheets:
            row = await _get_gsheet_row_by_cell_value(
                worksheet=w,
                cell_value=cell_value
            )
            if row: 
                break
    else:
        w = gsheet.worksheet('title', worksheet_title)
        row = await _get_gsheet_row_by_cell_value(
            worksheet=w,
            cell_value=cell_value
        )
    return row


async def get_data(
    gsheet: pygsheets.Spreadsheet, 
    search_data: list,
    worksheet_title: str | None = None
) -> list[SheetRowTenderContent]:
    # TODO: Отрефакторить до O(1) по памяти (менять исходный список)
    rows = []
    for data in search_data:
        row = await get_gsheet_row_by_cell_value(
            gsheet=gsheet,
            cell_value=data,
            worksheet_title=worksheet_title
        )
        if row:
            rows.append(row)
    return rows
