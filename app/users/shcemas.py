from pydantic import BaseModel, EmailStr


class User(BaseModel):
    password: str
    username: str
    email: EmailStr


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
