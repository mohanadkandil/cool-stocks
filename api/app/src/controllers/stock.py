from fastapi import HTTPException
from typing import Any
from datetime import datetime, timedelta
import asyncio

from ..config import settings
from .. import schemas
from .base import BaseController

class StockController(BaseController):
    def updateStockPriceAttributes(self, stock):
        updateFlag = False
        if datetime.utcnow() - datetime.fromisoformat(stock['highestPriceLastUpdate']) > timedelta(minutes=settings.STOCK_PRICE_TIME_FRAME):
            stock['highestPrice'] = stock['price']
            stock['highestPriceLastUpdate'] = datetime.utcnow().isoformat()
            updateFlag = True
        if datetime.utcnow() - datetime.fromisoformat(stock['lowestPriceLastUpdate']) > timedelta(minutes=settings.STOCK_PRICE_TIME_FRAME):
            stock['lowestPrice'] = stock['price']
            stock['lowestPriceLastUpdate'] = datetime.utcnow().isoformat()
            updateFlag = True
        return updateFlag

    def getStock(self, stock_id: str) -> Any:
        url = 'stock/'
        queryParams = { 'stock_id': stock_id }
        stocks = super().request(payload={}, queryParams=queryParams, url=url, method='get')
        if not stocks:
            return
        stock_need_update = self.updateStockPriceAttributes(stocks[0])
        if stock_need_update:
            updated_stock = super().request(payload={**stocks[0]}, queryParams={}, url='stock/', method='put')
            return updated_stock
        else:
            return stocks[0]
        

    def checkTransactionFound(self, requestBody, method):
        queryParams = {
            'stock_id': requestBody.stock_id,
            'user_id': requestBody.user_id,
            'amount': requestBody.total,
            'upper_bound': requestBody.upperBound,
            'lower_bound': requestBody.lowerBound,
            'transaction_success': False,
            'transaction_pending': True,
            'action': method
        }
        transactionFound = super().request(payload={}, queryParams=queryParams, url='transaction/', method='get')
        if transactionFound:
            raise HTTPException(
                status_code=400,
                detail='There is a transaction found with same specs, we will try to execute it for you shortly',
            )
        return

    async def retryTransaction(self, transaction):
        await asyncio.sleep(settings.RETRY_TRANSACTION_COMMIT_TIME_FRAME)   # try async function to retry buy/sell again after a period of time
        stocks = super().request(payload={}, queryParams={ 'stock_id': transaction['stock_id'] }, url='stock/', method='get')
        if not stocks:
            # notify user stock no longer available
            return
        transaction['transaction_success'] = True
        transaction['transaction_pending'] = False
        transaction['price_per_stock'] = stocks[0]['price']
        if transaction['upper_bound'] < stocks[0]['price'] or transaction['lower_bound'] > stocks[0]['price']:
            transaction['transaction_success'] = False
        updated_transaction = super().request(payload={**transaction}, queryParams={}, url='transaction/', method='put')
        # ... notify user either transaction success/failure for second transaction attempt


    async def buyStock(self, requestBody: schemas.BuyStock) -> Any:
        self.checkTransactionFound(requestBody=requestBody, method='buy')
        stocks = super().request(payload={}, queryParams={ 'stock_id': requestBody.stock_id }, url='stock/', method='get')
        users = super().request(payload={}, queryParams={ 'id': requestBody.user_id }, url='user/', method='get')
        if not stocks or not users:
            raise HTTPException(
                status_code=404,
                detail='Not Found',
            )
        if requestBody.total > stocks[0]['availability'] or (stocks[0]['price'] * requestBody.total > users[0]['amount']):
            raise HTTPException(
                status_code=400,
                detail='Bad Request',
            )
        transactionSuccess = True
        transactionStillPending = False
        if requestBody.upperBound < stocks[0]['price'] or requestBody.lowerBound > stocks[0]['price']:
            transactionSuccess = False
            transactionStillPending = True
        payload = {
            'stock_id': requestBody.stock_id,
            'user_id': requestBody.user_id,
            'amount': requestBody.total,
            'price': stocks[0]['price'],
            'transaction_success': transactionSuccess,
            'transaction_pending': transactionStillPending,
            'upper_bound': requestBody.upperBound,
            'lower_bound': requestBody.lowerBound,
            'action': 'buy'
        }
        new_transaction = super().request(payload=payload, queryParams={}, url='transaction/', method='post')
        if not transactionSuccess:
            task = asyncio.create_task(self.retryTransaction(new_transaction))
            return { 'message': 'Transaction will be executed again shortly as stock price is out of bounds'}
        return { 'message': 'Transaction Success'}


    async def sellStock(self, requestBody: schemas.SellStock) -> Any:
        self.checkTransactionFound(requestBody=requestBody, method='sell')
        users = super().request(payload={}, queryParams={ 'id': requestBody.user_id }, url='user/', method='get')
        stocks = super().request(payload={}, queryParams={ 'stock_id': requestBody.stock_id }, url='stock/', method='get')
        if not stocks or not users:
            raise HTTPException(
                status_code=404,
                detail='Not Found',
            )
        transactionSuccess = True
        transactionStillPending = False        
        if requestBody.upperBound < stocks[0]['price'] or requestBody.lowerBound > stocks[0]['price']:
            transactionSuccess = False
            transactionStillPending = True
        payload = {
            'stock_id': requestBody.stock_id,
            'user_id': requestBody.user_id,
            'amount': requestBody.total,
            'price': stocks[0]['price'],
            'transaction_success': transactionSuccess,
            'transaction_pending': transactionStillPending,
            'upper_bound': requestBody.upperBound,
            'lower_bound': requestBody.lowerBound,
            'action': 'sell'
        }        
        new_transaction = super().request(payload=payload, queryParams={}, url='transaction/', method='post')
        if not transactionSuccess:
            task = asyncio.create_task(self.retryTransaction(new_transaction))
            return { 'message': 'Transaction will be executed again shortly as stock price is out of bounds'}
        return { 'message': 'Transaction Success'}

stock = StockController()
