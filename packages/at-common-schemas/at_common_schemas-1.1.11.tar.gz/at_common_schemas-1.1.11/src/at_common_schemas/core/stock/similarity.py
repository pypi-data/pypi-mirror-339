from pydantic import Field
from at_common_schemas.base import BaseSchema

class Similarity(BaseSchema):
    symbol_base: str = Field(..., description="Base stock symbol")
    symbol_peer: str = Field(..., description="Peer stock symbol")
    score_description: float = Field(..., description="Text-based description similarity score between 0 and 1")
    score_market_cap: float = Field(..., description="Market capitalization similarity score between 0 and 1")
    score_composite: float = Field(..., description="Overall combined similarity score between 0 and 1")