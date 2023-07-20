"""DB connection library

MySQLManager:
    - 유저 정보 저장을 위한 EC2 MySQL DB Manager 입니다.
    Functions:
        - insert_user_auth: 유저의 계정 정보를 저장합니다.
        - delete_user_auth: 유저의 계정 정보를 삭제합니다.
        - get_user_auth: 유저의 계정 정보를 가져옵니다.
        - get_user_all_auth_number: DB에 저장된 모든 계정의 전화번호를 가져옵니다.

Raises:
    MySQLManagerError: MySQLManager에서 발생한 오류

"""
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
        """Insert user auth info to user_auth table.
        Args:
            phone_number: user phone_number
            password: user decryption password
        
        Return:
            phone_number
            
        Raise:
            Failed to insert user auth on DB.
        """
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
        """Delete user auth info from user_auth table.
        Args:
            phone_number: user phone_number
        
        Return:
            phone_number
            
        Raise:
            Failed to delete user auth on DB.
        """
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
        """Get user auth info from user_auth table.
        Args:
            phone_number: user phone_number
        
        Return:
            {"phone_number": phone_number, "password": password}
            
        Raise:
            Failed to get user auth on DB.
        """
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
    
    def get_user_all_auth_number(self) -> list:
        """Get all user auth info from user_auth table.
        Return:
            [phone_number, ...]
            
        Raise:
            Failed to get all user auth phone_number on DB.
        """
        try:
            all_user_auth_number = list()
            with self.session as session:
                sql = select(User)
                for obj in session.execute(sql):
                    all_user_auth_number.append(obj.User.phone_number)
            return all_user_auth_number
        except Exception:
            raise MySQLManagerError("Failed to get all user auth phone_number on DB.")
        
    

class MySQLManagerError(Exception):
    """All DBManager Error"""

