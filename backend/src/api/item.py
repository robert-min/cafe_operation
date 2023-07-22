from fastapi import APIRouter, Header
from pydantic import BaseModel
from api import CustomHttpException
from lib.util import make_respose
from lib.db_connect import MySQLManager, MySQLManagerError
from lib.validator import ApiValidator, BadRequestError, UnAuthorizationError

item_router = APIRouter(prefix="/item")
ApiValidator = ApiValidator()
MySQLManager = MySQLManager()

class Item(BaseModel):
    category: str
    selling_price: int
    cost_price: int
    name: str
    description: str
    barcode: str
    expiration_date: str
    size: str


@item_router.post("/")
async def insert_item(item: Item, user: str = Header(None), authorization: str = Header(None)):
    try:
        # check user login
        ApiValidator.check_current_user(user, authorization)
        
        # check user valid input(expriation_date, size)
        ApiValidator.check_user_valid_input(item.expiration_date, item.size)
        
        # Insert user item in DB
        result = MySQLManager.insert_item_info(user, item.dict())
        return make_respose({"phone_number": result, "name": item.name})
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except MySQLManagerError as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")


@item_router.delete("/{seq}")
async def delete_item(seq: int, user: str = Header(None), authorization: str = Header(None)):
    try:
        # check user login
        ApiValidator.check_current_user(user, authorization)
        
        # Delete user item in DB
        result = MySQLManager.delete_item_info(user, seq)
        return make_respose(result)
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except MySQLManagerError as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")


@item_router.get("/{seq}")
async def get_item(seq: int, user: str = Header(None), authorization: str = Header(None)):
    try:
        # check user login
        ApiValidator.check_current_user(user, authorization)
        
        # Delete user item in DB
        result = MySQLManager.get_item_info(user, seq)
        return make_respose(result)
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except MySQLManagerError as e:
        raise CustomHttpException(500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(500, error=e, message="Unknown error. Contact service manager.")
    
