import re
from .db_connect import MySQLManager


class ApiValidator:
    def __init__(self) -> None:
        self.MySQLManager = MySQLManager()
        
    def check_user_signup(self, phone_number: str) -> None:
        if not re.match(r"\d{3}-\d{4}-\d{4}", phone_number):
            raise BadRequestError("The input does not fit the phone number format.")
        
        all_user_phone_number = self.MySQLManager.get_user_all_auth_number()
        if phone_number in all_user_phone_number:
            raise BadRequestError("This phone number already exists. Please log in with your existing account.")
        
        
        
class BadRequestError(Exception):
    """Bad Request Error : 400"""