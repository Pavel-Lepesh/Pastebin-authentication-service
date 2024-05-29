from fastapi import APIRouter, Depends, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend_db.db_depends import get_db
from app.users.shcemas import User, UserPublic, AccessTokenSchema
from app.users.dao import UsersDAO
from app.users.shcemas import Tokens
from app.auth_utils import create_tokens
from app.users.auth import get_authenticate_user, check_token
from typing import Annotated
from app.exceptions import UserAlreadyExists


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/all')
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]) -> list[UserPublic]:
    users = await UsersDAO.get_all_users(db)
    return users


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Annotated[AsyncSession, Depends(get_db)]) -> Tokens:
    exist_user = await UsersDAO.get_user(db, username=user.username)
    if exist_user:
        raise UserAlreadyExists
    user = await UsersDAO.create_user(user, db)
    tokens = create_tokens(user=user)
    await UsersDAO.update_refresh_token(user.id, tokens.refresh_token, db)
    return tokens


@router.post("/tokens", status_code=status.HTTP_200_OK)
async def get_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    db: Annotated[AsyncSession, Depends(get_db)]) -> Tokens:
    user = await get_authenticate_user(form_data.username, form_data.password, db)
    tokens = create_tokens(user=user)
    await UsersDAO.update_refresh_token(user.id, tokens.refresh_token, db)
    response.set_cookie(key="pastebin_refresh_token", value=tokens.refresh_token, httponly=True)
    response.set_cookie(key="pastebin_access_token", value=tokens.access_token, httponly=True)
    return tokens


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_and_get_new_tokens(refresh_token: str, db: Annotated[AsyncSession, Depends(get_db)]) -> Tokens:
    user = await check_token(refresh_token, db, refresh=True)
    tokens = create_tokens(user=user)
    await UsersDAO.update_refresh_token(user.id, tokens.refresh_token, db)
    return tokens


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_access_token(token: AccessTokenSchema, db: Annotated[AsyncSession, Depends(get_db)]):
    await check_token(token.access_token, db)


@router.get("/test_get")
async def me_func(request: Request):
    print("From print", {"Get test succeeded": "ura", "headers": request.headers})
    return {"Get test succeeded": "ura", "headers": request.headers}


@router.post("/test_post")
async def func(request: Request):
    return request.headers
