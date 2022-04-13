from fastapi import APIRouter, Response, HTTPException
from typing import Optional

from .. import schemas
from .. import controllers

userRouter = APIRouter()

@userRouter.get('/{id}', status_code=200, response_model=schemas.User)
def get_user(
    id: int,
    response: Response,
) -> Optional[schemas.User]:
    userFound = controllers.user.getUser(id)
    if not userFound:
        raise HTTPException(status_code=404, detail=f'User with id {id} not found')
    return userFound


@userRouter.post('/', status_code=201, response_model=schemas.User)
def create_user(
    requestBody: schemas.UserCreate,
) -> schemas.User:
    createdUser = controllers.user.createUser(requestBody)
    return createdUser


@userRouter.put('/deposit', status_code=200, response_model=schemas.User)
def deposit_amount(
    requestBody: schemas.UserDeposit,
) -> schemas.User:
    updatedUser = controllers.user.deposit(requestBody)
    if not updatedUser:
        raise HTTPException(status_code=400, detail='Failed to update user')
    return updatedUser


@userRouter.put('/withdraw', status_code=200, response_model=schemas.User)
def withdraw_amount(
    requestBody: schemas.UserWithdraw,
) -> schemas.User:
    updatedUser = controllers.user.withdraw(requestBody)
    if not updatedUser:
        raise HTTPException(status_code=400, detail='Failed to update user')
    return updatedUser