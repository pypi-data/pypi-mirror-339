"""
Core API client for the AT Backend Data service.
"""
import logging
from typing import List
from datetime import datetime
from at_common_schemas.core.candlestick import Interval as CandlestickInterval
from at_common_schemas.core.news import Category
from ..schema.quote import (
    QuoteGetRequest, QuoteGetResponse, QuoteBatchGetRequest, QuoteBatchGetResponse
)
from ..schema.news import (
    NewsListRequest, NewsListResponse,
    NewsSearchRequest, NewsSearchResponse,
)
from ..schema.candlestick import (
    CandlestickListRequest, CandlestickListResponse
)
from ..schema.entry import (
    StockListResponse,
    ExchangeListResponse,
    SectorListResponse,
    IndustryListResponse,
    CountryListResponse,
)
from ..schema.stock.company import (
    CompanyProfileGetRequest, CompanyProfileGetResponse
)
from ..schema.stock.analyst import (
    PriceTargetSummaryGetRequest, PriceTargetSummaryGetResponse,
    PriceTargetConsensusGetRequest, PriceTargetConsensusGetResponse,
    GradeDetailListRequest, GradeDetailListResponse,
    GradeSummaryListRequest, GradeSummaryListResponse,
    GradeConsensusGetRequest, GradeConsensusGetResponse
)
from ..schema.stock.calendar import (
    CalendarEarningsListRequest, CalendarEarningsListResponse,
    CalendarDividendsListRequest, CalendarDividendsListResponse,
    CalendarSplitsListRequest, CalendarSplitsListResponse,
)
from ..schema.stock.financial import (
    IncomeListRequest, IncomeListResponse,
    BalanceSheetListRequest, BalanceSheetListResponse,
    CashFlowListRequest, CashFlowListResponse,
    IncomeGrowthListRequest, IncomeGrowthListResponse,
    BalanceSheetGrowthListRequest, BalanceSheetGrowthListResponse,
    CashFlowGrowthListRequest, CashFlowGrowthListResponse,
    ComprehensiveGrowthListRequest, ComprehensiveGrowthListResponse,
    MetricsListRequest, MetricsListResponse,
    MetricsTTMGetRequest, MetricsTTMGetResponse,
    RatiosListRequest, RatiosListResponse,
    RatiosTTMGetRequest, RatiosTTMGetResponse,
    StatementPeriod
)

from .base import BaseClient

logger = logging.getLogger(__name__)

class CoreClient(BaseClient):
    """Client for the AT Backend Data Core API."""
    
    def __init__(self, host: str, port: int):
        """
        Initialize the Core API client.
        
        Args:
            host: Host name
            port: Port number
        """
        super().__init__(host, port)
        self.base_url = f"{self.base_url}/core"

    #
    # Quote API
    #
    async def quote_get(self, symbol: str) -> QuoteGetResponse:
        """
        Get stock quote for a single symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Quote data
        """
        request = QuoteGetRequest(symbol=symbol)
        response_data = await self.post("quote/get", json=request.model_dump())
        return QuoteGetResponse(**response_data)
    
    async def quote_batch_get(self, symbols: List[str]) -> QuoteBatchGetResponse:
        """
        Get stock quotes for multiple symbols.
        
        Args:
            symbols: List of stock symbols (e.g., ['AAPL', 'MSFT'])
            
        Returns:
            Batch quote data
        """
        request = QuoteBatchGetRequest(symbols=symbols)
        response_data = await self.post("quote/batch-get", json=request.model_dump())
        return QuoteBatchGetResponse(**response_data)
    
    #
    # News API
    #
    async def news_list(
        self, 
        category: Category, 
        date_from: datetime, 
        date_to: datetime, 
        limit: int = 50
    ) -> NewsListResponse:
        """
        Get latest news by category.
        
        Args:
            category: News category (GENERAL, STOCK, CRYPTO, FOREX)
            date_from: Start date
            date_to: End date
            limit: Maximum number of news items to return
            
        Returns:
            News list response
        """
        request = NewsListRequest(
            category=category,
            date_from=date_from,
            date_to=date_to,
            limit=limit
        )
        response_data = await self.post("news/list", json=request.model_dump())
        return NewsListResponse(**response_data)
    
    async def news_search(
        self, 
        symbol: str, 
        date_from: datetime, 
        date_to: datetime, 
        limit: int = 50
    ) -> NewsSearchResponse:
        """
        Search news for a specific symbol.
        
        Args:
            symbol: Stock symbol
            date_from: Start date
            date_to: End date
            limit: Maximum number of news items to return
            
        Returns:
            News search response
        """
        request = NewsSearchRequest(
            symbol=symbol,
            date_from=date_from,
            date_to=date_to,
            limit=limit
        )
        response_data = await self.post("news/search", json=request.model_dump())
        return NewsSearchResponse(**response_data)
    
    #
    # Candlestick API
    #
    async def candlestick_list(
        self, 
        symbol: str, 
        interval: CandlestickInterval,
        from_time: datetime,
        to_time: datetime
    ) -> CandlestickListResponse:
        """
        Get candlestick data for a symbol.
        
        Args:
            symbol: Stock symbol
            interval: Time interval for candlestick data
            from_time: Start time
            to_time: End time
            
        Returns:
            Candlestick data
        """
        request = CandlestickListRequest(
            symbol=symbol,
            interval=interval,
            from_time=from_time,
            to_time=to_time
        )
        response_data = await self.post("candlestick/list", json=request.model_dump())
        return CandlestickListResponse(**response_data)
    
    #
    # Entry API
    #
    async def entry_stock_list(self) -> StockListResponse:
        """
        Get list of available stocks.
        
        Returns:
            Stock list data
        """
        response_data = await self.post("entry/stock/list", json={})
        return StockListResponse(**response_data)
    
    async def entry_exchange_list(self) -> ExchangeListResponse:
        """
        Get list of available exchanges.
        
        Returns:
            Exchange list data
        """
        response_data = await self.post("entry/exchange/list", json={})
        return ExchangeListResponse(**response_data)
    
    async def entry_sector_list(self) -> SectorListResponse:
        """
        Get list of available sectors.
        
        Returns:
            Sector list data
        """
        response_data = await self.post("entry/sector/list", json={})
        return SectorListResponse(**response_data)
    
    async def entry_industry_list(self) -> IndustryListResponse:
        """
        Get list of available industries.
        
        Returns:
            Industry list data
        """
        response_data = await self.post("entry/industry/list", json={})
        return IndustryListResponse(**response_data)
    
    async def entry_country_list(self) -> CountryListResponse:
        """
        Get list of available countries.
        
        Returns:
            Country list data
        """
        response_data = await self.post("entry/country/list", json={})
        return CountryListResponse(**response_data)
    
    #
    # Stock - Company API
    #
    async def stock_company_profile_get(self, symbol: str) -> CompanyProfileGetResponse:
        """
        Get company profile for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Company profile data
        """
        request = CompanyProfileGetRequest(symbol=symbol)
        response_data = await self.post("stock/company/profile/get", json=request.model_dump())
        return CompanyProfileGetResponse(**response_data)
    
    #
    # Stock - Analyst API
    #
    async def stock_analyst_price_target_summary_get(self, symbol: str) -> PriceTargetSummaryGetResponse:
        """
        Get price target summary for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Price target summary data
        """
        request = PriceTargetSummaryGetRequest(symbol=symbol)
        response_data = await self.post("stock/analyst/price-target/summary/get", json=request.model_dump())
        return PriceTargetSummaryGetResponse(**response_data)
    
    async def stock_analyst_price_target_consensus_get(self, symbol: str) -> PriceTargetConsensusGetResponse:
        """
        Get price target consensus for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Price target consensus data
        """
        request = PriceTargetConsensusGetRequest(symbol=symbol)
        response_data = await self.post("stock/analyst/price-target/consensus/get", json=request.model_dump())
        return PriceTargetConsensusGetResponse(**response_data)
    
    async def stock_analyst_grade_detail_list(self, symbol: str, limit: int = 50) -> GradeDetailListResponse:
        """
        Get analyst grade details for a symbol.
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of items to return
            
        Returns:
            Grade detail list data
        """
        request = GradeDetailListRequest(symbol=symbol, limit=limit)
        response_data = await self.post("stock/analyst/grade/detail/list", json=request.model_dump())
        return GradeDetailListResponse(**response_data)
    
    async def stock_analyst_grade_summary_list(self, symbol: str, limit: int = 50) -> GradeSummaryListResponse:
        """
        Get analyst grade summary for a symbol.
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of items to return
            
        Returns:
            Grade summary list data
        """
        request = GradeSummaryListRequest(symbol=symbol, limit=limit)
        response_data = await self.post("stock/analyst/grade/summary/list", json=request.model_dump())
        return GradeSummaryListResponse(**response_data)
    
    async def stock_analyst_grade_consensus_get(self, symbol: str) -> GradeConsensusGetResponse:
        """
        Get analyst grade consensus for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Grade consensus data
        """
        request = GradeConsensusGetRequest(symbol=symbol)
        response_data = await self.post("stock/analyst/grade/consensus/get", json=request.model_dump())
        return GradeConsensusGetResponse(**response_data)
    
    #
    # Stock - Calendar API
    #
    async def stock_calendar_earnings_list(self, symbol: str, limit: int = 50) -> CalendarEarningsListResponse:
        """
        Get earnings calendar data for a symbol.
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of items to return
            
        Returns:
            Earnings calendar data
        """
        request = CalendarEarningsListRequest(symbol=symbol, limit=limit)
        response_data = await self.post("stock/calendar/earnings/list", json=request.model_dump())
        return CalendarEarningsListResponse(**response_data)
    
    async def stock_calendar_dividends_list(self, symbol: str, limit: int = 50) -> CalendarDividendsListResponse:
        """
        Get dividends calendar data for a symbol.
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of items to return
            
        Returns:
            Dividends calendar data
        """
        request = CalendarDividendsListRequest(symbol=symbol, limit=limit)
        response_data = await self.post("stock/calendar/dividends/list", json=request.model_dump())
        return CalendarDividendsListResponse(**response_data)
    
    async def stock_calendar_splits_list(self, symbol: str, limit: int = 50) -> CalendarSplitsListResponse:
        """
        Get stock splits data for a symbol.
        
        Args:
            symbol: Stock symbol
            limit: Maximum number of items to return
            
        Returns:
            Stock splits data
        """
        request = CalendarSplitsListRequest(symbol=symbol, limit=limit)
        response_data = await self.post("stock/calendar/splits/list", json=request.model_dump())
        return CalendarSplitsListResponse(**response_data)
    
    #
    # Stock - Financial API
    #
    async def stock_financial_income_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> IncomeListResponse:
        """
        Get income statements for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Income statement data
        """
        request = IncomeListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/income/list", json=request.model_dump())
        return IncomeListResponse(**response_data)
    
    async def stock_financial_balance_sheet_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> BalanceSheetListResponse:
        """
        Get balance sheet statements for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Balance sheet statement data
        """
        request = BalanceSheetListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/balance_sheet/list", json=request.model_dump())
        return BalanceSheetListResponse(**response_data)
    
    async def stock_financial_cash_flow_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> CashFlowListResponse:
        """
        Get cash flow statements for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Cash flow statement data
        """
        request = CashFlowListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/cash_flow/list", json=request.model_dump())
        return CashFlowListResponse(**response_data)
    
    async def stock_financial_income_growth_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> IncomeGrowthListResponse:
        """
        Get income statement growth data for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Income statement growth data
        """
        request = IncomeGrowthListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/income/growth/list", json=request.model_dump())
        return IncomeGrowthListResponse(**response_data)
    
    async def stock_financial_balance_sheet_growth_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> BalanceSheetGrowthListResponse:
        """
        Get balance sheet growth data for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Balance sheet growth data
        """
        request = BalanceSheetGrowthListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/balance_sheet/growth/list", json=request.model_dump())
        return BalanceSheetGrowthListResponse(**response_data)
    
    async def stock_financial_cash_flow_growth_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> CashFlowGrowthListResponse:
        """
        Get cash flow growth data for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Cash flow growth data
        """
        request = CashFlowGrowthListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/cash_flow/growth/list", json=request.model_dump())
        return CashFlowGrowthListResponse(**response_data)
    
    async def stock_financial_comprehensive_growth_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> ComprehensiveGrowthListResponse:
        """
        Get comprehensive financial growth data for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Comprehensive growth data
        """
        request = ComprehensiveGrowthListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/comprehensive/growth/list", json=request.model_dump())
        return ComprehensiveGrowthListResponse(**response_data)
    
    async def stock_financial_metrics_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> MetricsListResponse:
        """
        Get financial metrics for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Financial metrics data
        """
        request = MetricsListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/metrics/list", json=request.model_dump())
        return MetricsListResponse(**response_data)
    
    async def stock_financial_metrics_ttm_get(self, symbol: str) -> MetricsTTMGetResponse:
        """
        Get trailing twelve months (TTM) metrics for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            TTM metrics data
        """
        request = MetricsTTMGetRequest(symbol=symbol)
        response_data = await self.post("stock/financial/metrics/ttm/get", json=request.model_dump())
        return MetricsTTMGetResponse(**response_data)
    
    async def stock_financial_ratios_list(
        self, symbol: str, period: StatementPeriod, limit: int = 50
    ) -> RatiosListResponse:
        """
        Get financial ratios for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Period type (ANNUAL, QUARTERLY)
            limit: Maximum number of items to return
            
        Returns:
            Financial ratios data
        """
        request = RatiosListRequest(symbol=symbol, period=period, limit=limit)
        response_data = await self.post("stock/financial/ratios/list", json=request.model_dump())
        return RatiosListResponse(**response_data)
    
    async def stock_financial_ratios_ttm_get(self, symbol: str) -> RatiosTTMGetResponse:
        """
        Get trailing twelve months (TTM) ratios for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            TTM ratios data
        """
        request = RatiosTTMGetRequest(symbol=symbol)
        response_data = await self.post("stock/financial/ratios/ttm/get", json=request.model_dump())
        return RatiosTTMGetResponse(**response_data) 