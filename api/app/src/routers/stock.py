from fastapi import APIRouter, Response, HTTPException
from typing import Optional, Any

from .. import schemas
from .. import controllers

stockRouter = APIRouter()

@stockRouter.get('/{stock_id}', status_code=200, response_model=schemas.Stock)
def get_stock(
    stock_id: str,
    response: Response,
) -> Optional[schemas.Stock]:
    stockFound = controllers.stock.getStock(stock_id)
    if not stockFound:
        raise HTTPException(status_code=404, detail=f'Stock with id {stock_id} not found')
    return stockFound


@stockRouter.post('/buy', status_code=200)
async def buy_stock(
    requestBody: schemas.BuyStock,
) -> Any:
    message = await controllers.stock.buyStock(requestBody)
    return message


@stockRouter.post('/sell', status_code=200)
async def sell_stock(
    requestBody: schemas.SellStock,
) -> Any:
    message = await controllers.stock.sellStock(requestBody)
    return message
