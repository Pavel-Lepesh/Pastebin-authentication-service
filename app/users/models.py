from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from app.backend_db.db import Base
from datetime import datetime, timezone


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    date_joined: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))
    refresh_token: Mapped[str] = mapped_column(nullable=True)
