from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.quote import Quote
from typing import List

# Quote
class QuoteGetRequest(BaseSchema):
    symbol: str = Field(..., description="ticker symbol")

class QuoteGetResponse(Quote):
    pass

class QuoteBatchGetRequest(BaseSchema):
    symbols: List[str] = Field(..., description="List of ticker symbols")

class QuoteBatchGetResponse(BaseSchema):
    items: List[Quote] = Field(..., description="List of quotes")