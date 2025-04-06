from at_common_schemas.base import BaseSchema
from at_common_schemas.core.stock.company import Profile
from pydantic import Field

class CompanyProfileGetRequest(BaseSchema):
    """Request for a company profile."""
    symbol: str = Field(..., description="The stock symbol for which the profile is requested.")

class CompanyProfileGetResponse(Profile):
    """Response containing stock profile information."""
    pass