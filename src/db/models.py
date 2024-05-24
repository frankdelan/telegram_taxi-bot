import enum
from datetime import datetime

from sqlalchemy import BigInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Status(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    CANCEL = 'cancel'

    def __str__(self) -> str:
        return self.value


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    number: Mapped[str]


class Driver(Base):
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    number: Mapped[str]
    car_model: Mapped[str]
    car_color: Mapped[str]
    car_number: Mapped[str]


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    address_from: Mapped[str]
    address_to: Mapped[str]
    date = mapped_column(TIMESTAMP, default=datetime.now())
    id_user: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[Status]
    id_order_message: Mapped[int] = mapped_column(BigInteger, default=0)
