from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from . import MYSQL_CONNECTION
from model import User


class MySQLManager:
    """
    MySQL DB manager
    """
    def __init__(self) -> None:
        user = MYSQL_CONNECTION['user']
        passwd = MYSQL_CONNECTION['password']
        host = MYSQL_CONNECTION['host']
        port = MYSQL_CONNECTION['port']
        db = MYSQL_CONNECTION['db']
        charset = MYSQL_CONNECTION['charset']
        engine = create_engine(
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?{charset}",
            echo=False, pool_size=10, pool_recycle=500, max_overflow=10)

        self.session = Session(engine)

    def insert_user_auth(self, phone_number: str, password: bytes) -> str:
        try:
            with self.session as session:
                content = User(
                    phone_number=phone_number,
                    password=password,
                    timestamp=datetime.utcnow()
                )
                session.add(content)
                session.commit()
            return phone_number
        except Exception:
            raise MySQLManagerError("Failed to insert user auth on DB.")
    
    def delete_user_auth(self, phone_number: str) -> str:
        try:
            with self.session as session:
                sql = select(User).filter(User.phone_number == phone_number)
                user_auth = session.execute(sql).scalar_one()
                if user_auth:
                    session.delete(user_auth)
                session.commit()
            return phone_number
        except Exception:
            raise MySQLManagerError("Failed to delete user auth on DB.")
    
    def get_user_auth(self, phone_number: str) -> dict:
        try:
            with self.session as session:
                sql = select(User).filter(User.phone_number == phone_number)
                obj = session.execute(sql).scalar_one()
                return {
                    "phone_number": obj.phone_number,
                    "password": obj.password
                }
        except Exception:
            raise MySQLManagerError("Failed to get user auth on DB.")
    
    

class MySQLManagerError(Exception):
    """All DBManager Error"""

