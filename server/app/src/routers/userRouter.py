from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import db
from .. import controllers
from .. import schemas  

userRouter = APIRouter()
mn = 'User'

@userRouter.get('/', status_code=200)
async def get(id: int = None, email: str = None, db: Session = Depends(db.get_db)):
    if id:
        load = { 'id': id }
    elif email:
        load = { 'email': email}
    else:
        load = {}
    return await controllers.dbRequests.get(params=load, mn=mn, db=db)

@userRouter.post('/', status_code=201)
async def createUser(body: schemas.CreateUser, db: Session = Depends(db.get_db)):
    return await controllers.dbRequests.post(body=body, mn=mn, db=db)


@userRouter.put('/', status_code=200)
async def updateUser(body: schemas.UpdateUser, db: Session = Depends(db.get_db)):
    return await controllers.dbRequests.put(body=body, mn=mn, db=db)