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
        return f"User(email={self.email}, name={self.name})"
