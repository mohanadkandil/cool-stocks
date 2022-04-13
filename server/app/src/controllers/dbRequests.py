from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Any

from .. import models

class dbRequestsController():
    def getModel(self, modelName):
        if modelName == 'User':
            return models.User
        if modelName == 'Stock':
            return models.Stock
        if modelName == 'Transaction':
            return models.Transaction

    async def get(self, mn: str, params: dict, db: Session) -> Any:
        model = self.getModel(mn)
        return db.query(model).filter_by(**params).all()

    async def post(self, mn: str, body, db: Session) -> Any:
        model = self.getModel(mn)
        new_entry = model(**body.__dict__)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry

    async def put(self, mn: str, body, db: Session) -> Any:
        model = self.getModel(mn)
        objFound = db.query(model).filter(model.id==body.id).first()
        if objFound is None:
            return
        for var, value in vars(body).items():
            setattr(objFound, var, value) if value else None
        db.add(objFound)
        db.commit()
        db.refresh(objFound)
        return objFound

    async def createTransaction(self, body, db: Session) -> Any:
        new_transaction = models.Transaction(
            user_id=body.user_id,
            stock_id=body.stock_id,
            transaction_success=body.transaction_success,
            transaction_pending=body.transaction_pending,
            price_per_stock=body.price,
            upper_bound=body.upper_bound,
            lower_bound=body.lower_bound,
            stock_amount=body.amount,
            action=body.action
        )
        db.add(new_transaction)
        if not body.transaction_pending:
            user = db.query(models.User).filter(models.User.id==body.user_id).first()
            if body.action == 'buy':
                user.amount -= body.price * body.amount
            else:
                user.amount += body.price * body.amount                    
            db.add(user)
            
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
        
    async def updateTransaction(self, body, mn, db: Session):
        transactions = await self.get(mn=mn, params={'id': body.id}, db=db)
        if not transactions:
            return
        for var, value in vars(body).items():
            setattr(transactions[0], var, value)
        db.add(transactions[0])
        if body.transaction_success:
            user = db.query(models.User).filter(models.User.id==body.user_id).first()
            if body.action == 'buy':
                user.amount -= body.price_per_stock * body.stock_amount
            else:
                user.amount += body.price_per_stock * body.stock_amount                    
            db.add(user)
        db.commit()
        db.refresh(transactions[0])
        return transactions[0]

    async def delete(self, body, db: Session) -> Any:
        return

dbRequests = dbRequestsController()