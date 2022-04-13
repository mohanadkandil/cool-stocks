from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Any

from .. import schemas
from .. import adapters
from .base import BaseController

class UserController(BaseController):
    def getUser(self, id: int) -> Any:
        url = 'user/'
        queryParams = { 'id': id }
        users = super().request(payload={}, queryParams=queryParams, url=url, method='get')
        if users:
            return users[0]
        return


    def getUserByEmail(self, email: str) -> Any:
        url = 'user/'
        queryParams = { 'email': email }
        userFound = super().request(payload={}, queryParams=queryParams, url=url, method='get')
        return userFound


    def createUser(self, requestBody: schemas.UserCreate) -> Any:
        users = self.getUserByEmail(requestBody.email)
        if users:
            raise HTTPException(
                status_code=400,
                detail="This user already exists in the system.",
            )
        payload = {
            **requestBody.__dict__,
            'amount': 0,
        }                
        new_user = super().request(payload=payload, queryParams={}, url='user/', method='post')
        return new_user
            

    def deposit(self, requestBody: schemas.UserDeposit) -> Any:
        if requestBody.amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid amount execution")
        userFound = self.getUser(requestBody.id)
        if not userFound:
            raise HTTPException(status_code=404, detail="Invalid user ID")
        userFound['amount'] += requestBody.amount
        updated_user = super().request(payload={**userFound}, queryParams={}, url='user/', method='put')
        return updated_user


    def withdraw(self, requestBody: schemas.UserWithdraw) -> Any:
        if requestBody.amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid amount execution")
        userFound = self.getUser(requestBody.id)
        if not userFound:
            raise HTTPException(status_code=404, detail="Invalid user ID")
        if requestBody.amount > userFound['amount']:
            raise HTTPException(status_code=400, detail="No Funds")
        userFound['amount'] -= requestBody.amount
        updated_user = super().request(payload={**userFound}, queryParams={}, url='user/', method='put')
        return updated_user

user = UserController()
