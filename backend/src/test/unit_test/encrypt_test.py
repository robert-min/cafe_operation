from unittest import TestCase
from enum import Enum
from lib.encrypt import EncryptManager

EncryptManager = EncryptManager()

class Mock(Enum):
    PASSWORD = "123adfabv22"
    

class EncryptTestCase(TestCase):
    def test_encrypt_decrypt_pasword(self):
        encrypt_password = EncryptManager.encrypt_password(Mock.PASSWORD.value)
        self.assertEqual(type(encrypt_password), bytes)
        
        decrypt_password = EncryptManager.decrypt_password(encrypt_password)
        self.assertEqual(decrypt_password, Mock.PASSWORD.value)