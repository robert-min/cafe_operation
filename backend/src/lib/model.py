from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import VARCHAR


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_auth"
    
    seq: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    timestamp: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    
    def __repr__(self) -> str:
        return f"User(phone_number={self.phone_number})"


class Item(Base):
    __tablename__ = "user_item"
    
    seq: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    category: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    selling_price: Mapped[int] = mapped_column(nullable=False)
    cost_price: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR(1000), nullable=True)
    barcode:  Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    expiration_date: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    size: Mapped[str] = mapped_column(VARCHAR(100), nullable=False) # small/ large
    search_initial: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    
    def __repr__(self) -> str:
        return f"Item(name={self.name})"
