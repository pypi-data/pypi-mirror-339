from pydantic import Field
from at_common_schemas.base import BaseSchema
from datetime import datetime

class Profile(BaseSchema):
    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Full legal name of the company")
    currency: str | None = Field(None, description="Currency in which the stock is traded")
    exchange: str = Field(..., description="Abbreviated name of the stock exchange")
    sector: str | None = Field(None, description="Broader market sector classification")
    industry: str | None = Field(None, description="Industry classification of the company")
    description: str | None = Field(None, description="Brief overview of the company's business")
    country: str | None = Field(None, description="Country where the company is headquartered")
    image: str | None = Field(None, description="URL to company logo or image")
    ipo_date: datetime | None = Field(None, description="Date of initial public offering")