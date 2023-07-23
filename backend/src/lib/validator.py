"""Api validate library

ApiValidator:
    - API 호출 수 유효성 검사를 진행하는 라이브러리입니다.
    Functions:
        - check_user_signup: 회원가입을 위해 유저가 입력한 값을 검사합니다.
        - check_user_login: 로그인을 위해 유저가 입력한 값을 검사합니다.
        - check_user_valid_input: 아이템 등록을 위해 유저가 입력한 값을 검사합니다.
        - check_current_user: 사용자의 토큰이 유효한지 확인합니다.

Raises:
    BadRequestError: 400
    UnAuthorizationError: 401
"""
import re
import jwt
from . import TOKEN_KEY
from .db_connect import MySQLManager
from .encrypt import EncryptManager


class ApiValidator:
    def __init__(self) -> None:
        self.MySQLManager = MySQLManager()
        self.EncryptManager = EncryptManager()
        
    def check_user_signup(self, phone_number: str) -> None:
        """Check user valid signup input
        Args:
            phone_number: user phone_number

        Raise:
            phone_number format error: The input does not fit the phone number format.
            phon_number already existence error: 
                This phone number already exists. Please log in with your existing account.
        """
        if not re.match(r"\d{3}-\d{4}-\d{4}", phone_number):
            raise BadRequestError("The input does not fit the phone number format.")
        
        all_user_phone_number = self.MySQLManager.get_user_all_auth_number()
        if phone_number in all_user_phone_number:
            raise BadRequestError("This phone number already exists. Please log in with your existing account.")
    
    def check_user_login(self, phone_number: str, password: str) -> None:
        """Check user valid signup input
        Args:
            phone_number: user phone_number
            password: user password

        Raise:
            phone_number format error: The input does not fit the phone number format.
            phon_number no existence error: Invalid phone number. Please check your phone number.
            wrong password error: Wrong password. Please check your password.
        """
        if not re.match(r"\d{3}-\d{4}-\d{4}", phone_number):
            raise BadRequestError("The input does not fit the phone number format.")
        
        all_user_phone_number = self.MySQLManager.get_user_all_auth_number()
        if phone_number not in all_user_phone_number:
            raise BadRequestError("Invalid phone number. Please check your phone number.")
        
        encrypt_password = self.MySQLManager.get_user_auth(phone_number)["password"]
        decrypt_password = self.EncryptManager.decrypt_password(encrypt_password)
        if password != decrypt_password:
            raise UnAuthorizationError("Wrong password. Please check your password.")
    
    def check_user_valid_input(self, expriation_date: str=None, size: str=None) -> None:
        """Check user valid input for insert item
        Args:
            expriation_date: item expriation_date
            size: item size

        Raise:
            expriation_date format error: The input does not fit the expriation date format.
            size format error: The input does not fit the size format. (small or large)
        """
        if expriation_date and not re.match(r"\d{4}-\d{2}-\d{2}", expriation_date):
            raise BadRequestError("The input does not fit the expriation date format.")
        if size and size not in ["small", "large"]:
            raise BadRequestError("The input does not fit the size format. (small or large)")
    
    def check_current_user(self, user: str, token: str) -> None:
        """Check current valid user
        Args:
            user: user phone_number headers value
            token: login jwt token

        Raise:
            token no existence error: Token does not exist.
            token not match error: The wrong approach. Go back to the previous page
            token expired error: An expired token. Please log in again.
        """
        # check token existence
        if token is None:
            raise BadRequestError("Token does not exist.")
        # check token expired period
        try:
            decode_token = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
            # check wrong used token
            if decode_token["phone_number"] != user:
                raise UnAuthorizationError("The wrong approach. Go back to the previous page")
        except jwt.ExpiredSignatureError:
            raise UnAuthorizationError("An expired token. Please log in again.")

        
        
class BadRequestError(Exception):
    """Bad Request Error : 400"""
    

class UnAuthorizationError(Exception):
    """UnAuthorization Error : 401"""