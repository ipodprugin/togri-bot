from pydantic import BaseModel


class SheetRowTenderContent(BaseModel):
    id: str
    address: str | None = None
    subway_stations: str | None = None
    region_name: str | None = None
    district_name: str | None = None
    object_area: float | None = None
    floor: str | None = None
    applications_enddate: str | None = None
    deposit: str | None = None
    start_price: str | None = None
    m1_start_price: float | None = None
    imgzippath: str | None = None
    min_price: float | None = None
    m1_min_price: str | None = None
    procedure_form: int | None = None
    auction_step: str | None = None
    price_decrease_step: str | None = None
    tendering: str | None = None
    lat: str | None = None
    lon: str | None = None
