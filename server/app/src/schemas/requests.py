from typing import Optional
from pydantic import BaseModel

class request(BaseModel):
    modelName: str
    filters: dict

class CreateStock(BaseModel):
    id: str
    name: str
    price: int
    availability: int
    highestPrice: int
    lowestPrice: int
    highestPriceLastUpdate: str
    lowestPriceLastUpdate: str
    timestamp: str

class UpdateStock(BaseModel):
    id: Optional[str]
    name: Optional[str]
    price: Optional[int]
    availability: Optional[int]
    highestPrice: Optional[int]
    lowestPrice: Optional[int]
    highestPriceLastUpdate: Optional[str]
    lowestPriceLastUpdate: Optional[str]
    timestamp: Optional[str]

class CreateTransaction(BaseModel):
    stock_id: str
    user_id: int
    amount: int
    price: float
    transaction_success: bool
    transaction_pending: bool
    upper_bound: float
    lower_bound: float
    action: str

class UpdateTransaction(BaseModel):
    id: int
    stock_id: str
    user_id: int
    stock_amount: int
    price_per_stock: float
    transaction_success: bool
    transaction_pending: bool
    upper_bound: float
    lower_bound: float
    action: str

class CreateUser(BaseModel):
    full_name: str
    email: str
    password: str
    amount: float

class UpdateUser(BaseModel):
    id: int
    amount: float

class response(BaseModel):
    class Config():
        orm_mode = True