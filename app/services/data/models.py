from pydantic import BaseModel


class SheetRowTenderContent(BaseModel):
    tender_id: str
    address: str | None = None
    subway_stations: str | None = None
    region_name: str | None = None
    district_name: str | None = None
    object_area: float | None = None
    floor: str | None = None
    applications_enddate: str | None = None
    deposit: float | None = None
    start_price: float | None = None
    m1_start_price: float | None = None
    imgzippath: str | None = None
    min_price: float | None = None
    m1_min_price: float | None = None
    procedure_form: str | None = None
    auction_step: float | None = None
    price_decrease_step: float | None = None
    tendering: str | None = None
    lat: float | None = None
    lon: float | None = None
    entrance_type: str | None = None
    windows: str | None = None
    ceilings: str | None = None
