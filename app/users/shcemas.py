from pydantic import BaseModel, EmailStr


class User(BaseModel):
    password: str
    username: str
    email: EmailStr


class UserPublic(BaseModel):
    email: EmailStr
    username: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenSchema(BaseModel):
    access_token: str
