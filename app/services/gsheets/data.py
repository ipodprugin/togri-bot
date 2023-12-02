import pygsheets

from .models import SheetRowTenderContent


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
            m1_start_price = '{:0.2f}'.format(float(m1_start_price)) if m1_start_price else None
            start_price = '{:0.2f}'.format(float(start_price)) if start_price else None

            row = SheetRowTenderContent(
                id=row[1],
                address=row[2],
                region_name=row[3],
                district_name=row[4],
                object_area=row[-10],
                floor=row[8],
                applications_enddate=row[10],
                deposit=row[7],
                start_price=start_price,
                m1_start_price=m1_start_price,
            )
            return row
        except IndexError as e:
            print(f'При обработке строки с {cell_value} произошла ошибка: {e}')


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
