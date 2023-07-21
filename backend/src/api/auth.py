from fastapi import APIRouter
from pydantic import BaseModel
from api import CustomHttpException
from lib.util import make_respose
from lib.validator import ApiValidator, BadRequestError
from lib.db_connect import MySQLManager, MySQLManagerError
from lib.encrypt import EncryptManager, EncryptManagerError


class User(BaseModel):
    phone_number: str
    password: str

ApiValidator = ApiValidator()
EncryptManager = EncryptManager()
MySQLManager = MySQLManager()
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/signup")
def signup_user(user: User):
    try:
        # check user input validate
        ApiValidator.check_user_signup(user.phone_number)
        
        # encrypt password
        encrypt_password = EncryptManager.encrypt_password(user.password)
        
        # Insert user auth in DB
        result = MySQLManager.insert_user_auth(user.phone_number, encrypt_password)
        return make_respose(result)
    except BadRequestError as e:
        raise CustomHttpException(400, error=e, message="Please check your phone number.")
    except (MySQLManagerError, EncryptManagerError) as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")

