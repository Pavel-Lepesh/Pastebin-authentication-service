from app.users.models import Users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from app.users.shcemas import User
from app.auth_utils import get_password_hash


class UsersDAO:
    model = Users

    @classmethod
    async def create_user(cls, user_data: User, db: AsyncSession):
        hashed_password = get_password_hash(user_data.password)
        query = (
            insert(cls.model)
            .values(
                username=user_data.username,
                hashed_password=hashed_password,
                email=user_data.email
            )
        )

        await db.execute(query)
        await db.commit()

        user = await UsersDAO.get_user(db, username=user_data.username)
        return user

    @classmethod
    async def get_user(cls, db: AsyncSession, **filter_by):
        query = (
            select(cls.model)
            .filter_by(**filter_by)
        )
        user = await db.scalar(query)
        return user

    @classmethod
    async def get_all_users(cls, db: AsyncSession):
        query = (
            select(cls.model)
        )
        users = await db.scalars(query)
        return users.all()

    @classmethod
    async def delete_user(cls, db: AsyncSession, user_id):
        query = (
            delete(cls.model)
            .where(cls.model.id == user_id)
        )
        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_user_refresh_token(cls, db: AsyncSession, **filter_by):
        query = (
            select(cls.model.refresh_token)
            .filter_by(**filter_by)
        )
        refresh_token = await db.scalar(query)
        return refresh_token

    @classmethod
    async def update_refresh_token(cls, user_id: int, refresh_token: str, db: AsyncSession):
        query = (
            update(cls.model)
            .values(refresh_token=refresh_token)
            .where(cls.model.id == user_id)
        )
        await db.execute(query)
        await db.commit()
