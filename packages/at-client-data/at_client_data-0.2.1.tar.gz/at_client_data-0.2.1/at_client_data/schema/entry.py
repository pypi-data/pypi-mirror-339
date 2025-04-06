from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.entry import Stock, Exchange, Sector, Industry, Country

# Symbol
class StockListRequest(BaseSchema):
    pass

class StockListResponse(BaseSchema):
    items: List[Stock] = Field(..., description="List of symbols")

# Exchange
class ExchangeListRequest(BaseSchema):
    pass

class ExchangeListResponse(BaseSchema):
    items: List[Exchange] = Field(..., description="List of exchanges")

# Sector
class SectorListRequest(BaseSchema):
    pass

class SectorListResponse(BaseSchema):
    items: List[Sector] = Field(..., description="List of sectors")

# Industry
class IndustryListRequest(BaseSchema):
    pass

class IndustryListResponse(BaseSchema):
    items: List[Industry] = Field(..., description="List of industries")

# Country
class CountryListRequest(BaseSchema):
    pass

class CountryListResponse(BaseSchema):
    items: List[Country] = Field(..., description="List of countries")