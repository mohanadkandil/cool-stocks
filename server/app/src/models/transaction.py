from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from datetime import datetime

from .. import db

class Transaction(db.Base):
    __tablename__ = 'transactions'
    id = Column(Integer, name="id", primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(String, ForeignKey('stocks.id'))
    transaction_pending = Column(Boolean, nullable=False, default=False)
    transaction_success = Column(Boolean, nullable=False, default=False)
    order_time = Column(DateTime, nullable=False, default=datetime.utcnow())
    stock_amount = Column(Integer, nullable=False)
    price_per_stock = Column(Float, nullable=False)
    upper_bound = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=False)
    action = Column(String, nullable=False)