from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.users.models import Users
from app.users.shcemas import Tokens
from app.exceptions import CredentialsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_token(token: str, secret_key: str) -> dict:
    try:
        payload = jwt.decode(token[7:], secret_key, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise CredentialsError


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_tokens(user: Users,
                  access_expires_delta: timedelta = timedelta(minutes=settings.JWT_DEFAULT_EXPIRES_MINUTES),
                  refresh_expires_delta: timedelta = timedelta(days=settings.JWT_DEFAULT_EXPIRES_DAYS)) -> Tokens:
    access_expire = datetime.now(timezone.utc) + access_expires_delta
    refresh_expire = datetime.now(timezone.utc) + refresh_expires_delta
    to_encode = {
        "user_id": user.id,
        "is_superuser": user.is_superuser,
        "exp": access_expire
    }
    access_token = "Bearer " + jwt.encode(to_encode, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    to_encode.update(exp=refresh_expire)
    refresh_token = "Bearer " + jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return Tokens(access_token=access_token, refresh_token=refresh_token)
