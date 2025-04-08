from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime
from enum import Enum

class DividendPeriod(str, Enum):
	QUARTERLY = "QUARTERLY"
	ANNUAL = "ANNUAL"
	SEMI_ANNUAL = "SEMI_ANNUAL"
	SPECIAL = "SPECIAL"
	MONTHLY = "MONTHLY"
	WEEKLY = "WEEKLY"
	UNKNOWN = "UNKNOWN"

class Dividends(BaseSchema):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: datetime = Field(..., description="Date when the dividend was issued")
	record_date: datetime | None = Field(..., description="Date by which investors must be on company records to receive the dividend")
	payment_date: datetime | None = Field(..., description="Date when the dividend payment is distributed to shareholders")
	declaration_date: datetime | None = Field(..., description="Date when the company's board announces the dividend")
	adj_dividend: float = Field(..., description="Dividend amount adjusted for stock splits and similar events")
	dividend: float = Field(..., description="Unadjusted dividend amount per share")
	yield_value: float = Field(..., description="dividend expressed as a percentage of the stock price")
	frequency: DividendPeriod | None = Field(None, description="How often dividends are paid (e.g., quarterly, annually, special)")

class Earnings(BaseSchema):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: datetime = Field(..., description="Date of the earnings announcement")
	eps_actual: float | None = Field(None, description="Actual earnings per share reported")
	eps_estimated: float | None = Field(None, description="Analysts' consensus estimate for earnings per share")
	revenue_actual: float | None = Field(None, description="Actual revenue reported by the company")
	revenue_estimated: float | None = Field(None, description="Analysts' consensus estimate for company revenue")

class Splits(BaseSchema):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: datetime = Field(..., description="Date when the stock split occurred")
	numerator: int | float = Field(..., description="Top number in the split ratio (e.g., 2 in a 2:1 split)")
	denominator: int | float = Field(..., description="Bottom number in the split ratio (e.g., 1 in a 2:1 split)")