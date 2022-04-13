from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import db
from .. import controllers
from .. import schemas

stockRouter = APIRouter()
mn = 'Stock'

@stockRouter.get('/', status_code=200)
async def getStock(
    stock_id: str,
    db: Session = Depends(db.get_db)
):
    params = { 'id': stock_id }
    return await controllers.dbRequests.get(params=params, mn=mn, db=db)


@stockRouter.post('/', status_code=201)
async def createStock(
    body: schemas.CreateStock,
    db: Session = Depends(db.get_db)
):
    return await controllers.dbRequests.post(body=body, mn=mn, db=db)


@stockRouter.put('/', status_code=200)
async def updateStock(
    body: schemas.UpdateStock,
    db: Session = Depends(db.get_db)
):
    return await controllers.dbRequests.put(body=body, mn=mn, db=db)
    