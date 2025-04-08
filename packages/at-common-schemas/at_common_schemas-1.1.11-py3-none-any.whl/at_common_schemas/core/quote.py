from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime

class Quote(BaseSchema):
	symbol: str = Field(..., description="Stock ticker symbol")
	price: float = Field(..., description="Current market price")
	change_percentage: float = Field(..., description="Percentage price change from previous close")
	change: float = Field(..., description="Absolute price change from previous close")
	volume: int = Field(..., description="Trading volume for the current session")
	day_low: float = Field(..., description="Lowest price reached during current trading day")
	day_high: float = Field(..., description="Highest price reached during current trading day")
	year_high: float = Field(..., description="Highest price reached in the past 52 weeks")
	year_low: float = Field(..., description="Lowest price reached in the past 52 weeks")
	market_cap: int = Field(..., description="Total market capitalization in base currency")
	time: datetime = Field(..., description="time of the quote")

class PriceChange(BaseSchema):
	symbol: str = Field(..., description="Stock ticker symbol")
	one_day: float = Field(..., description="Percentage price change over the past day")
	five_day: float = Field(..., description="Percentage price change over the past 5 trading days")
	one_month: float = Field(..., description="Percentage price change over the past month")
	three_month: float = Field(..., description="Percentage price change over the past 3 months")
	ytd: float = Field(..., description="Percentage price change year-to-date")
	one_year: float = Field(..., description="Percentage price change over the past year")
	three_year: float = Field(..., description="Percentage price change over the past 3 years")
	five_year: float = Field(..., description="Percentage price change over the past 5 years")
	ten_year: float = Field(..., description="Percentage price change over the past 10 years")
	max: float = Field(..., description="Maximum percentage price change since inception")