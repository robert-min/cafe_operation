import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel
from api import CustomHttpException
from lib import TOKEN_KEY
from lib.util import make_respose
from lib.db_connect import MySQLManager, MySQLManagerError
from lib.encrypt import EncryptManager, EncryptManagerError
from lib.validator import ApiValidator, BadRequestError, UnAuthorizationError

class User(BaseModel):
    phone_number: str
    password: str

ApiValidator = ApiValidator()
EncryptManager = EncryptManager()
MySQLManager = MySQLManager()
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/signup")
async def signup_user(user: User):
    try:
        # check user input signup validate
        ApiValidator.check_user_signup(user.phone_number)

        # encrypt password
        encrypt_password = EncryptManager.encrypt_password(user.password)
        
        # Insert user auth in DB
        result = MySQLManager.insert_user_auth(user.phone_number, encrypt_password)
        return make_respose(result)
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except (MySQLManagerError, EncryptManagerError) as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")


@auth_router.post("/login")
async def login_user(user: User):
    try:
        # check user input login validate
        ApiValidator.check_user_login(user.phone_number, user.password)
        
        # make JWT token
        token = jwt.encode({
                "email": user.phone_number,
                "exp": datetime.utcnow() + timedelta(hours=2)
            }, TOKEN_KEY, algorithm="HS256")
        return make_respose({"phone_number": user.phone_number,"token": token})
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except (MySQLManagerError, EncryptManagerError) as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")

