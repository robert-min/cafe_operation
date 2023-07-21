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
from sqlalchemy import create_engine, select, or_, and_
from sqlalchemy.orm import Session
from . import MYSQL_CONNECTION
from model import User, Item
from util import extract_korean_initial


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
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset={charset}",
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
            return "success"
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
            raise MySQLManagerError(
                "Failed to get all user auth phone_number on DB.")

    def insert_item_info(self, phone_number: str, params: dict) -> str:
        try:
            with self.session as session:
                content = Item(
                    phone_number=phone_number,
                    category=params["category"],
                    selling_price=int(params["selling_price"]),
                    cost_price=int(params["cost_price"]),
                    name=params["name"],
                    description=params["description"],
                    barcode=params["barcode"],
                    expiration_date=params["expiration_date"],
                    size=params["size"],
                    search_initial=extract_korean_initial(params["name"])
                )
                session.add(content)
                session.commit()
            return phone_number
        except Exception:
            raise MySQLManagerError("Failed to insert item info on DB.")

    def delete_item_info(self, phone_number: str, seq: int) -> str:
        try:
            with self.session as session:
                sql = select(Item).filter(Item.phone_number ==
                                          phone_number, Item.seq == seq)
                item_info = session.execute(sql).scalar_one()
                if item_info:
                    session.delete(item_info)
                session.commit()
            return "success"
        except Exception:
            raise MySQLManagerError("Failed to delete item info on DB.")

    def update_item_info(self, phone_number: str, seq: int, params: dict) -> str:
        try:
            with self.session as session:
                sql = select(Item).filter(Item.phone_number == phone_number,
                                          Item.seq == seq)
                item_obj = session.execute(sql).scalar_one()
                for key, value in params.items():
                    if type(value) is str:
                        exec(f"item_obj.{key} = '{value}'")
                    else:
                        exec(f"item_obj.{key} = int({value})")
                    if key == "name":
                        item_obj.search_initial = extract_korean_initial(value)
                session.commit()
            return list(params.keys())
        except Exception:
            raise MySQLManagerError("Failed to update item info on DB")

    def get_item_info(self, phone_number: str, seq: int) -> list:
        try:
            with self.session as session:
                sql = select(Item).filter(Item.phone_number == phone_number,
                                          Item.seq == seq)
                obj = session.execute(sql).scalar_one()
                return {
                    "phone_number": obj.phone_number,
                    "category": obj.category,
                    "selling_price": obj.selling_price,
                    "cost_price": obj.cost_price,
                    "name": obj.name,
                    "description": obj.description,
                    "barcode": obj.barcode,
                    "expiration_date": obj.expiration_date,
                    "size": obj.size
                }
        except Exception:
            raise MySQLManagerError("Failed to get item info on DB.")

    def get_all_item(self, phone_number: str) -> list:
        try:
            all_item = list()
            with self.session as session:
                sql = select(Item).filter(Item.phone_number == phone_number)
                for obj in session.execute(sql):
                    all_item.append({
                        "phone_number": obj.Item.phone_number,
                        "category": obj.Item.category,
                        "selling_price": obj.Item.selling_price,
                        "cost_price": obj.Item.cost_price,
                        "name": obj.Item.name,
                        "description": obj.Item.description,
                        "barcode": obj.Item.barcode,
                        "expiration_date": obj.Item.expiration_date,
                        "size": obj.Item.size
                    })
            return all_item
        except Exception:
            raise MySQLManagerError("Failed to get all item info on DB")

    def get_search_item(self, phone_number: str, keyword: str) -> list:
        try:
            search_item = list()
            with self.session as session:
                sql = select(Item).filter(and_(Item.phone_number == phone_number, or_(
                    Item.name.like(keyword + '%'), Item.search_initial.like(keyword + '%'))))
                for obj in session.execute(sql):
                    search_item.append({
                        "phone_number": obj.Item.phone_number,
                        "category": obj.Item.category,
                        "selling_price": obj.Item.selling_price,
                        "cost_price": obj.Item.cost_price,
                        "name": obj.Item.name,
                        "description": obj.Item.description,
                        "barcode": obj.Item.barcode,
                        "expiration_date": obj.Item.expiration_date,
                        "size": obj.Item.size
                    })
            return search_item
        except Exception:
            raise MySQLManagerError("Failed to get search item info on DB")


class MySQLManagerError(Exception):
    """All DBManager Error"""
