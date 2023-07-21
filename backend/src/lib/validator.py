import re
from .db_connect import MySQLManager
from .encrypt import EncryptManager


class ApiValidator:
    def __init__(self) -> None:
        self.MySQLManager = MySQLManager()
        self.EncryptManager = EncryptManager()
        
    def check_user_signup(self, phone_number: str) -> None:
        if not re.match(r"\d{3}-\d{4}-\d{4}", phone_number):
            raise BadRequestError("The input does not fit the phone number format.")
        
        all_user_phone_number = self.MySQLManager.get_user_all_auth_number()
        if phone_number in all_user_phone_number:
            raise BadRequestError("This phone number already exists. Please log in with your existing account.")
    
    def check_user_login(self, phone_number:str, password: str) -> None:
        if not re.match(r"\d{3}-\d{4}-\d{4}", phone_number):
            raise BadRequestError("The input does not fit the phone number format.")
        
        all_user_phone_number = self.MySQLManager.get_user_all_auth_number()
        if phone_number not in all_user_phone_number:
            raise BadRequestError("Invalid phone number. Please check your phone number.")
        
        encrypt_password = self.MySQLManager.get_user_auth(phone_number)["password"]
        decrypt_password = self.EncryptManager.decrypt_password(encrypt_password)
        if password != decrypt_password:
            raise UnAuthorizationError("Wrong password. Please check your password.")
        
        
class BadRequestError(Exception):
    """Bad Request Error : 400"""
    

class UnAuthorizationError(Exception):
    """UnAuthorization Error : 401"""