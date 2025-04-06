from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.stock.analyst import (
    PriceTargetSummary, PriceTargetConsensus,
    GradeDetail, GradeSummary, GradeConsensus
)

# Price Target Summary
class PriceTargetSummaryGetRequest(BaseSchema):
    """Request for analyst price target summary."""
    symbol: str = Field(..., description="The stock symbol for the request.")

class PriceTargetSummaryGetResponse(PriceTargetSummary):
    """Response containing analyst price target summary."""
    pass

# Price Target Consensus
class PriceTargetConsensusGetRequest(BaseSchema):
    """Request for analyst price target consensus."""
    symbol: str = Field(..., description="The stock symbol for the request.")

class PriceTargetConsensusGetResponse(PriceTargetConsensus):
    """Response containing analyst price target consensus."""
    pass

# Grade Detail
class GradeDetailListRequest(BaseSchema):
    """Request for analyst grades."""
    symbol: str = Field(..., description="The stock symbol for the request.")
    limit: int = Field(..., description="The number of results to return.")
    
class GradeDetailListResponse(BaseSchema):
    """Response containing analyst grades."""
    items: List[GradeDetail] = Field(..., description="List of analyst grades.")

# Grade Historical
class GradeSummaryListRequest(BaseSchema):
    """Request for analyst grades historical data."""
    symbol: str = Field(..., description="The stock symbol for the request.")
    limit: int = Field(..., description="The number of results to return.")

class GradeSummaryListResponse(BaseSchema):
    """Response containing analyst grades historical data."""
    items: List[GradeSummary] = Field(..., description="List of analyst grades historical data.")

# Grade Consensus
class GradeConsensusGetRequest(BaseSchema):
    """Request for analyst grades consensus."""
    symbol: str = Field(..., description="The stock symbol for the request.")

class GradeConsensusGetResponse(GradeConsensus):
    """Response containing analyst grades consensus."""
    pass