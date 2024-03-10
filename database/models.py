from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    ForeignKey,
    DateTime
)
from typing_extensions import Annotated
from typing import List
from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime
bigint = Annotated[int, 64]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            bigint: BigInteger
        }
    )


class User(Base):
    __tablename__ = 'users'
    id: Mapped[bigint] = mapped_column(unique=True, primary_key=True)
    status: Mapped[int] = mapped_column(default=0)
    date = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow())


class StickerPack(Base):
    __tablename__ = 'sets'
    name: Mapped[str] = mapped_column(unique=True, primary_key=True)
    owner_id: Mapped[bigint] = mapped_column(ForeignKey(User.id), primary_key=True)
    owner: Mapped[User] = relationship()
    title: Mapped[str]
    is_offered: Mapped[bool] = mapped_column(default=False)
    date: Mapped[bigint]


class Channel(Base):
    __tablename__ = 'channels'
    title: Mapped[str]
    channel_id: Mapped[bigint] = mapped_column(primary_key=True)
    link: Mapped[str]
    date = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow())
    subs: Mapped[int]
