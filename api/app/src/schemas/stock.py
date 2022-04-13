from typing import Optional, Union
from pydantic import BaseModel

class StockBase(BaseModel):
    id: Optional[str]
    name: Optional[str]
    price: Optional[int]
    availability: Optional[int]
    highestPrice: Optional[int]
    lowestPrice: Optional[int]
    highestPriceLastUpdate: Optional[str]
    lowestPriceLastUpdate: Optional[str]
    timestamp: Optional[str]

class Stock(StockBase):
    class Config():
        orm_mode = True

class StockCreate(BaseModel):
    stock_id: str
    name: str
    price: int
    availability: int
    timestamp: str

class BuyStock(BaseModel):
    stock_id: str
    user_id: int
    total: int
    upperBound: float
    lowerBound: float

class SellStock(BuyStock):
    pass