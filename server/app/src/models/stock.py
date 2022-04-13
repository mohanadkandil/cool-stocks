from sqlalchemy import Column, Integer, String

from .. import db
from ..config import settings
from .. import calc

class Stock(db.Base):
    __tablename__ = 'stocks'
    id = Column(String, name="id", primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, nullable=False)
    availability = Column(Integer, nullable=False)
    highestPrice = Column(Integer, nullable=False)
    lowestPrice = Column(Integer, nullable=False)
    highestPriceLastUpdate = Column(String, nullable=False)
    lowestPriceLastUpdate = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
# deal with stock before the stock update to db
calc.calcst(Stock)
