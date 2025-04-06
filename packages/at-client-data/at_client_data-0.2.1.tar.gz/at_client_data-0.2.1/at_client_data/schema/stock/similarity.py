from at_common_schemas.base import BaseSchema
from at_common_schemas.core.stock.similarity import Similarity
from pydantic import Field
from typing import List

class StockSimilarityListRequest(BaseSchema):
    """Request for a stock similarity list."""
    symbol: str = Field(..., description="The stock symbol for which the similarity list is requested.")
    limit: int = Field(10, description="The maximum number of similarities to return.")

class StockSimilarityListResponse(BaseSchema):
    """Response containing stock similarity information."""
    items: List[Similarity] = Field(..., description="The list of stock similarities.")