from datetime import datetime
from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.core.candlestick import Interval, Candlestick

class CandlestickListRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    from_time: datetime = Field(..., description="Start time for the request")
    to_time: datetime = Field(..., description="End time for the request")
    interval: Interval = Field(..., description="Interval for the request")

class CandlestickListResponse(BaseSchema):
    items: List[Candlestick] = Field(..., description="List of daily candlestick data")