from pydantic import BaseModel, Field, AfterValidator
from typing_extensions import Annotated
from datetime import datetime


class SheetRowTenderContent(BaseModel):
    tender_id: str
    address: str | None = None
    subway_stations: str | None = None
    region_name: str | None = None
    district_name: str | None = None
    object_area: Annotated[float | None, AfterValidator(lambda v: round(v, 2))] = None
    floor: str | None = None
    applications_enddate: datetime | None = None
    deposit: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    start_price: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    m1_start_price: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    imgzippath: str | None = None
    min_price: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    m1_min_price: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    procedure_form: str | None = None
    auction_step: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    price_decrease_step: Annotated[float | None, AfterValidator(lambda v: round(v, 2) if v else None)] = None
    tendering: datetime | None = None
    lat: float | None = None
    lon: float | None = None
    entrance_type: str | None = None
    windows: str | None = None
    ceilings: str | None = None

