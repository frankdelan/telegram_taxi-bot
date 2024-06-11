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


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram: Mapped[str]
    number: Mapped[str]
    is_auto: Mapped[bool]


class Driver(Base):
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    telegram: Mapped[str]
    phone_number: Mapped[str]


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    address_from: Mapped[str]
    address_to: Mapped[str]
    price: Mapped[float]
    date = mapped_column(TIMESTAMP, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status: Mapped[Status]
    id_user: Mapped[int] = mapped_column(BigInteger)
    id_order_message: Mapped[int] = mapped_column(BigInteger, default=0)
