from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth_utils import verify_password
from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import *
from datetime import datetime, timezone
from app.auth_utils import decode_token


async def get_authenticate_user(username: str, password: str, db: AsyncSession) -> Users:
    user = await UsersDAO.get_user(db, username=username)
    if not user:
        raise UserNotFound
    if not verify_password(password, user.hashed_password):
        raise IncorrectPassword
    return user


async def check_token(token: str, db: AsyncSession, refresh=False) -> Users | None:
    """
    Check various token's properties. Use refresh=True to check a refresh token.
    """
    token = token.strip('"')
    secret_key = settings.JWT_REFRESH_SECRET_KEY if refresh else settings.JWT_ACCESS_SECRET_KEY

    if not token.startswith("Bearer "):
        raise InvalidTypeOfToken

    try:
        payload = decode_token(token, secret_key)
    except JWTError:
        raise CredentialsError

    try:
        user_id, is_superuser, exp = payload["user_id"], payload["is_superuser"], payload["exp"]
    except KeyError:
        raise InvalidPayloadToken

    user = await UsersDAO.get_user(db, id=user_id)
    if not user:
        raise UserNotFound

    if datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
        raise ExpireTokenError

    if refresh:
        user_token_from_db = await UsersDAO.get_user_refresh_token(db, id=user_id)
        print(f"from_db {user_token_from_db}", f"current {token}", sep="\n")
        if user_token_from_db != token:
            raise FakeRefreshToken
    return user
