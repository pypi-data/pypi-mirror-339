from typing import List
from datetime import datetime
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.news import News, Category

class NewsListRequest(BaseSchema):
    category: Category = Field(..., description="The category of the news articles to retrieve")
    date_from: datetime = Field(..., description="The start date of the news articles to retrieve")
    date_to: datetime = Field(..., description="The end date of the news articles to retrieve")
    limit: int = Field(..., description="Maximum number of news articles to retrieve")

class NewsListResponse(BaseSchema):
    items: List[News] = Field(..., description="List of news articles")

class NewsSearchRequest(BaseSchema):
    symbol: str = Field(..., description="The stock ticker symbol to search for")
    date_from: datetime = Field(..., description="The start date of the news articles to retrieve")
    date_to: datetime = Field(..., description="The end date of the news articles to retrieve")
    limit: int = Field(..., description="Maximum number of news articles to retrieve")

class NewsSearchResponse(BaseSchema):
    items: List[News] = Field(..., description="List of stock-specific news articles")
