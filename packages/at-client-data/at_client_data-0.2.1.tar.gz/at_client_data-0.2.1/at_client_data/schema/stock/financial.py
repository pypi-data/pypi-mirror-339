from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.stock.financial import (
    StatementPeriod, 
    Income, BalanceSheet, CashFlow, 
    IncomeGrowth, BalanceSheetGrowth, CashFlowGrowth, ComprehensiveGrowth,
    Metrics, MetricsTTM, Ratios, RatiosTTM
)

# Batch request and response for financial income statements
class IncomeListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class IncomeListResponse(BaseSchema):
    items: List[Income] = Field(..., description="List of financial income statements.")

# Batch request and response for financial balance sheets statements
class BalanceSheetListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class BalanceSheetListResponse(BaseSchema):
    items: List[BalanceSheet] = Field(..., description="List of financial balance sheets statements.")

# Batch request and response for financial cash flows statements
class CashFlowListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class CashFlowListResponse(BaseSchema):
    items: List[CashFlow] = Field(..., description="List of financial cash flows statements.")

# Batch request and response for financial income statement growths
class IncomeGrowthListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class IncomeGrowthListResponse(BaseSchema):
    items: List[IncomeGrowth] = Field(..., description="List of financial income statement growths.")

# Batch request and response for financial balance sheet statement growths
class BalanceSheetGrowthListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class BalanceSheetGrowthListResponse(BaseSchema):
    items: List[BalanceSheetGrowth] = Field(..., description="List of financial balance sheet statement growths.")

# Batch request and response for financial cash flow statement growths
class CashFlowGrowthListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class CashFlowGrowthListResponse(BaseSchema):
    items: List[CashFlowGrowth] = Field(..., description="List of financial cash flow statement growths.")

# request and response for financial growths
class ComprehensiveGrowthListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit on the number of results returned.")

class ComprehensiveGrowthListResponse(BaseSchema):
    items: List[ComprehensiveGrowth] = Field(..., description="List of financial growths.")

# Batch request and response for financial key metrics
class MetricsListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class MetricsListResponse(BaseSchema):
    items: List[Metrics] = Field(..., description="List of key metrics for the stock.")

class MetricsTTMGetRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class MetricsTTMGetResponse(MetricsTTM):
    pass

# Batch request and response for financial ratios
class RatiosListRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the request.")
    period: StatementPeriod = Field(..., description="The period for the request.")
    limit: int = Field(..., description="The limit for the number of results.")

class RatiosListResponse(BaseSchema):
    items: List[Ratios] = Field(..., description="List of financial ratios for the stock.")

class RatiosTTMGetRequest(BaseSchema):
    symbol: str = Field(..., description="The stock symbol for the TTM request.")

class RatiosTTMGetResponse(RatiosTTM):
    pass