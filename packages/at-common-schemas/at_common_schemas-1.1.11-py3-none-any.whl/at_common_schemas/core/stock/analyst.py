from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime
from enum import Enum

# Enums
class GradeResult(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"

class GradeAction(str, Enum):
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"
    MAINTAIN = "MAINTAIN"

# Schemas
class PriceTargetSummary(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    last_month_count: int = Field(..., description="Number of price targets issued in the past month")
    last_month_avg_price_target: float = Field(..., description="Average of price targets from the past month")
    last_quarter_count: int = Field(..., description="Number of price targets issued in the past quarter")
    last_quarter_avg_price_target: float = Field(..., description="Average of price targets from the past quarter")
    last_year_count: int = Field(..., description="Number of price targets issued in the past year")
    last_year_avg_price_target: float = Field(..., description="Average of price targets from the past year")
    all_time_count: int = Field(..., description="Total number of price targets in the dataset")
    all_time_avg_price_target: float = Field(..., description="Average of all price targets in the dataset")

class PriceTargetConsensus(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    target_high: float = Field(..., description="Highest analyst price target currently active")
    target_low: float = Field(..., description="Lowest analyst price target currently active")
    target_consensus: float = Field(..., description="Average of all current analyst price targets")
    target_median: float = Field(..., description="Median value of all current analyst price targets")

class GradeDetail(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: datetime = Field(..., description="Date when the grade was issued")
    publisher: str = Field(..., description="Financial institution that issued the grade")
    previous_grade: GradeResult = Field(..., description="Previous grade assigned to the stock by this institution")
    current_grade: GradeResult = Field(..., description="New grade assigned to the stock by this institution")
    action: GradeAction = Field(..., description="Type of grade change (upgrade, downgrade, maintain, etc.)")

class GradeSummary(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: datetime = Field(..., description="Date of the historical rating snapshot")
    strong_buy_count: int = Field(..., description="Number of Strong Buy ratings at this point in time")
    buy_count: int = Field(..., description="Number of Buy ratings at this point in time")
    hold_count: int = Field(..., description="Number of Hold ratings at this point in time")
    sell_count: int = Field(..., description="Number of Sell ratings at this point in time")
    strong_sell_count: int = Field(..., description="Number of Strong Sell ratings at this point in time")

class GradeConsensus(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    strong_buy_count: int = Field(..., description="Current number of Strong Buy ratings")
    buy_count: int = Field(..., description="Current number of Buy ratings")
    hold_count: int = Field(..., description="Current number of Hold ratings")
    sell_count: int = Field(..., description="Current number of Sell ratings")
    strong_sell_count: int = Field(..., description="Current number of Strong Sell ratings")
    consensus: GradeResult = Field(..., description="Overall consensus rating based on all analyst ratings")