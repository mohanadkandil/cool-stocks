from sqlalchemy import event
from datetime import datetime, timedelta
from .config import settings

def calcst(Stock):
    @event.listens_for(Stock, 'before_update')
    def receive_before_update(mapper, connection, target):
        if datetime.fromisoformat(target.timestamp) - datetime.fromisoformat(target.highestPriceLastUpdate) > timedelta(minutes=settings.ST):
            target.highestPrice = target.price
            target.highestPriceLastUpdate = target.timestamp
        if datetime.fromisoformat(target.timestamp) - datetime.fromisoformat(target.lowestPriceLastUpdate) > timedelta(minutes=settings.ST):            
            target.lowestPrice = target.price
            target.lowestPriceLastUpdate = target.timestamp
        if target.highestPrice < target.price:
            target.highestPrice = target.price
            target.highestPriceLastUpdate = target.timestamp
        if target.lowestPrice > target.price:
            target.lowestPrice = target.price
            target.lowestPriceLastUpdate = target.timestamp
