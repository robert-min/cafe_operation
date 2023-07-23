from unittest import TestCase
from enum import Enum
from lib.db_connect import MySQLManager, MySQLManagerError
from sqlalchemy import select
from lib.model import Item


class MySQLManager(MySQLManager):
    def __init__(self) -> None:
        super().__init__()

    def get_item_seq(self, phone_number: str, name: str) -> str:
        try:
            with self.session as session:
                sql = select(Item).filter(Item.phone_number == phone_number, Item.name == name)
                obj = session.execute(sql).scalar_one()
            return obj.seq
        except Exception:
            raise MySQLManagerError("Failed to delete item info on DB.")
        


MySQLManager = MySQLManager()


class Mock(Enum):
    """Mock data for testing"""
    PHONE_NUMBER = "010-0000-0000"
    PASSWORD = "12312312"
    CATEGORY = "coffee"
    SELLING_PRICE = 5000
    COST_PRICE = 3500
    NAME = "아메리카노"
    DESCRIPTION = "맛있는 아메리카노"
    BARCODE = "010100000110224"
    EXPIRATION_DATE="2023-08-20"
    SIZE = "small"


class MySQLManagerAuthTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MySQLManager.insert_user_auth(Mock.PHONE_NUMBER.value, Mock.PASSWORD.value)
        print("\nSet up module for MySQLManager Auth testing lib/db_connect.py")

    def test_get_user_auth(self):
        result = MySQLManager.get_user_auth(Mock.PHONE_NUMBER.value)
        self.assertEqual(result["phone_number"], Mock.PHONE_NUMBER.value)
        self.assertEqual(result["password"], Mock.PASSWORD.value)
        
    def test_get_user_all_auth_number(self):
        result = MySQLManager.get_user_all_auth_number()
        self.assertIn(Mock.PHONE_NUMBER.value, result)
        
    @classmethod
    def tearDownClass(cls) -> None:
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)
        print("\nModule Clean.")


class MySQLManagerItemTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # single case test
        params = {
            "category": Mock.CATEGORY.value,
            "selling_price": Mock.SELLING_PRICE.value,
            "cost_price": Mock.COST_PRICE.value,
            "name": Mock.NAME.value,
            "description": Mock.DESCRIPTION.value,
            "barcode": Mock.BARCODE.value,
            "expiration_date": Mock.EXPIRATION_DATE.value,
            "size": Mock.SIZE.value
        }
        MySQLManager.insert_item_info(Mock.PHONE_NUMBER.value, params)
        
        # multi case test
        for i in range(11):
            params["name"] = Mock.NAME.value + str(i)
            MySQLManager.insert_item_info(Mock.PHONE_NUMBER.value, params)
        print("\nSet up module for MySQLManager Item testing lib/db_connect.py")
    
    @staticmethod
    def get_seq_num():
        return MySQLManager.get_item_seq(Mock.PHONE_NUMBER.value, Mock.NAME.value)
    
    def test_get_item_info(self):
        seq = self.get_seq_num()
        result = MySQLManager.get_item_info(Mock.PHONE_NUMBER.value, seq)
        self.assertEqual(result["selling_price"], Mock.SELLING_PRICE.value)
        self.assertEqual(result["description"], Mock.DESCRIPTION.value)
        self.assertEqual(result["expiration_date"], Mock.EXPIRATION_DATE.value)
    
    def test_update_item_info(self):
        seq = self.get_seq_num()
        change_params = {
            "category": "ice",
            "cost_price": 6000
        }
        result = MySQLManager.update_item_info(Mock.PHONE_NUMBER.value, seq, change_params)
        self.assertIn("category", result)
        self.assertIn("cost_price", result)
        
        result = MySQLManager.get_item_info(Mock.PHONE_NUMBER.value, seq)
        self.assertEqual(result["category"], change_params["category"])
        self.assertEqual(result["cost_price"], change_params["cost_price"])
        
    def test_get_all_item(self):
        result = MySQLManager.get_all_item(Mock.PHONE_NUMBER.value, page_number=1)
        self.assertTrue(result)
        
    def test_get_search_item(self):
        search_keyword = ["아메", "ㅇㅁㄹ", "아메리카", "ㅇㅁㄹㅋㄴ"]
        for keyword in search_keyword:
            result = MySQLManager.get_search_item(Mock.PHONE_NUMBER.value, keyword, page_number=1)
            self.assertTrue(result)
        
        seq = self.get_seq_num()
        change_params = {
            "name": "카페라떼"
        }
        result = MySQLManager.update_item_info(Mock.PHONE_NUMBER.value, seq, change_params)
        self.assertIn("name", result)
        search_keyword = ["카페라떼", "ㅋㅍ", "ㅋㅍㄹㄸ", "카페라"]
        for keyword in search_keyword:
            result = MySQLManager.get_search_item(Mock.PHONE_NUMBER.value, keyword, page_number=0)
            self.assertTrue(result)
        
        change_params = {
            "name": Mock.NAME.value
        }
        result = MySQLManager.update_item_info(Mock.PHONE_NUMBER.value, seq, change_params)
        self.assertIn("name", result)
        
    
    @classmethod
    def tearDownClass(cls) -> None:
        # single case test clean
        seq = MySQLManager.get_item_seq(Mock.PHONE_NUMBER.value, Mock.NAME.value)
        MySQLManager.delete_item_info(Mock.PHONE_NUMBER.value, seq)
        
        # multi case test clean
        for i in range(1, 12):
            MySQLManager.delete_item_info(Mock.PHONE_NUMBER.value, seq + i)
        print("\nModule Clean.")
    

