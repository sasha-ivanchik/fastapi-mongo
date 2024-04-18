from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import ENUM

from core.pydantic_models import Role


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(200), unique=True, nullable=False
    )
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, nullable=False)
    hashed_password: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    role: so.Mapped[Role] = so.mapped_column(
        ENUM(Role),
        default=Role.user,
    )
    hashed_token: so.Mapped["Token"] = relationship(back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    hashed_token: so.Mapped[str] = so.mapped_column(sa.String(1000), nullable=False)

    user: so.Mapped["User"] = relationship(back_populates="hashed_token")
