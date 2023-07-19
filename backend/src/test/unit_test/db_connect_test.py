import uuid
import base64
from unittest import TestCase
from enum import Enum
from lib.db_connect import MySQLManager

MySQLManager = MySQLManager()


class Mock(Enum):
    """Mock data for testing"""
    PHONE_NUMBER = "010-0000-0000"
    PASSWORD = "12312312"


class MySQLManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MySQLManager.insert_user_auth(Mock.PHONE_NUMBER.value, Mock.PASSWORD.value)
        print("\nSet up module for MySQLManager testing lib/db_connect.py")

    def test_get_user_auth(self):
        result = MySQLManager.get_user_auth(Mock.PHONE_NUMBER.value)
        self.assertEqual(result["phone_number"], Mock.PHONE_NUMBER.value)
        self.assertEqual(result["password"], Mock.PASSWORD.value)
        
    @classmethod
    def tearDownClass(cls) -> None:
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)
        print("\nModule Clean.")
    