from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend_db.db_depends import get_db
from app.users.shcemas import User
from app.users.dao import UsersDAO
from app.users.shcemas import Tokens
from app.auth_utils import create_tokens
from app.users.auth import get_authenticate_user, check_refresh_token
from typing import Annotated
from app.exceptions import UserAlreadyExists


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Annotated[AsyncSession, Depends(get_db)]):
    exist_user = await UsersDAO.get_user(db, username=user.username)
    if exist_user:
        raise UserAlreadyExists
    await UsersDAO.create_user(user, db)


@router.post("/tokens", status_code=status.HTTP_200_OK)
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    db: Annotated[AsyncSession, Depends(get_db)]) -> Tokens:
    user = await get_authenticate_user(form_data.username, form_data.password, db)
    tokens = create_tokens(user=user)
    await UsersDAO.update_refresh_token(user.id, tokens.refresh_token, db)
    return tokens


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_and_get_new_tokens(refresh_token: str, db: Annotated[AsyncSession, Depends(get_db)]) -> Tokens:
    user = await check_refresh_token(refresh_token, db)
    tokens = create_tokens(user=user)
    await UsersDAO.update_refresh_token(user.id, tokens.refresh_token, db)
    return tokens
