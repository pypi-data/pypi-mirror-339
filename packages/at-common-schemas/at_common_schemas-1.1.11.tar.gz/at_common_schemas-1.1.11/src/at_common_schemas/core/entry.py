from pydantic import Field
from at_common_schemas.base import BaseSchema

class AbstractEntry(BaseSchema):
    name: str = Field(..., description="name of the entry")

class Stock(AbstractEntry):
    symbol: str = Field(..., description="Stock ticker symbol used for identifying publicly traded companies")

class Exchange(AbstractEntry):
    pass

class Sector(AbstractEntry):
    pass

class Industry(AbstractEntry):
    pass

class Country(AbstractEntry):
    pass