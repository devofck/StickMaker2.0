from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from typing_extensions import Annotated
from typing import List
from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column
from sqlalchemy.orm import relationship

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
    status: Mapped[int]


class StickerPack(Base):
    __tablename__ = 'sets'
    name: Mapped[str] = mapped_column(unique=True, primary_key=True)
    owner_id: Mapped[bigint] = mapped_column(ForeignKey(User.id), primary_key=True)
    owner: Mapped[User] = relationship()
    title: Mapped[str]
    date: Mapped[bigint]

# class Settings(Base):
#     __tablename__ = 'sets'
