from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import db
from .. import controllers
from .. import schemas

transRouter = APIRouter()
mn = 'Transaction'

@transRouter.get('/', status_code=200)
async def getTransaction(
    stock_id: str,
    user_id: int,
    amount: int,
    transaction_success: bool,
    transaction_pending: bool,
    upper_bound: float,
    lower_bound: float,
    action: str,
    db: Session = Depends(db.get_db)
):
    params={
        'stock_id': stock_id,
        'user_id': user_id,
        'stock_amount': amount,
        'transaction_success': transaction_success,
        'transaction_pending': transaction_pending,
        'upper_bound': upper_bound,
        'lower_bound': lower_bound,
        'action': action
    }
    return await controllers.dbRequests.get(params=params, mn=mn, db=db)

@transRouter.get('/pending', status_code=200)
async def getPendingTransactions(transaction_pending: bool, transaction_success: bool, db: Session = Depends(db.get_db)):
    params = {
        'transaction_pending': transaction_pending,
        'transaction_success': transaction_success
    }
    return await controllers.dbRequests.get(params=params, mn=mn, db=db)
@transRouter.post('/', status_code=200)
async def createTransaction(body: schemas.CreateTransaction, db: Session = Depends(db.get_db)):
    return await controllers.dbRequests.createTransaction(body=body, db=db)
@transRouter.put('/', status_code=200)
async def updateTransaction(body: schemas.UpdateTransaction, db: Session = Depends(db.get_db)):
    return await controllers.dbRequests.updateTransaction(body=body, mn=mn, db=db)