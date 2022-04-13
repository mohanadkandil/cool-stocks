from pydantic import BaseModel

class StockCreate(BaseModel):
    stock_id: str
    name: str
    price: int
    availability: int
    timestamp: str