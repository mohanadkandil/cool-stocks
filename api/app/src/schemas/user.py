from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: Optional[int]
    full_name: Optional[str]
    email: Optional[str]
    amount: Optional[float]

class User(UserBase):
    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserDeposit(BaseModel):
    id: int
    amount: float

class UserWithdraw(UserDeposit):
    pass