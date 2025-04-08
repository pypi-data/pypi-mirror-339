from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime
from enum import Enum

class Interval(str, Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    EOD = "eod"

class Candlestick(BaseSchema):
    date: datetime = Field(..., description="Date of the price data")
    open: float = Field(..., description="Opening price for the trading day")
    high: float = Field(..., description="Highest price reached during the trading day")
    low: float = Field(..., description="Lowest price reached during the trading day")
    close: float = Field(..., description="Closing price for the trading day")
    volume: int = Field(..., description="Trading volume for the day")