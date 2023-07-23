from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import Optional
from api import CustomHttpException
from lib.util import make_respose
from lib.db_connect import MySQLManager, MySQLManagerError
from lib.validator import ApiValidator, BadRequestError, UnAuthorizationError

item_router = APIRouter(prefix="/item")
ApiValidator = ApiValidator()
MySQLManager = MySQLManager()


class CreateItem(BaseModel):
    category: str
    selling_price: int
    cost_price: int
    name: str
    description: str
    barcode: str
    expiration_date: str
    size: str


class UpdateItem(BaseModel):
    category: Optional[str] = None
    selling_price: Optional[int] = None
    cost_price: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    barcode: Optional[str] = None
    expiration_date: Optional[str] = None
    size: Optional[str] = None

@item_router.post("/")
async def insert_item(item: CreateItem, user: str = Header(None), authorization: str = Header(None)):
    """POST /item
    ## Insert item api
    It receives user(phone_number) and Authorization as Header values.
    And it receives category, selling_price, cost_price, name, description, barcode,
    expiration_date, and size as body values.
    
    ## Headers:
        user: user_phone_number
        authorization: login jwt token
    
    ## Body:
        **required params**
        category (str): item category
        selling_price (int): item selling price
        cost_price (int): item cost price
        name (str): item name
        description (str): item description
        barcode (str): item barcode
        expiration_date (str): item expiration_date **required format: 20XX-XX-XX**
        size (str): itme size **required format: small, large**
    
    ## Response:
        {
            "meta": {
                "code": 200,
                "message": "ok"
                },
            "data": {
                "phone_number": phone_number,
                "name": name
            }
        }
    """
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
        raise CustomHttpException(
            500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(
            500, error=e, message="Unknown error. Contact service manager.")


@item_router.delete("/{seq}")
async def delete_item(seq: int, user: str = Header(None), authorization: str = Header(None)):
    """Delete /item/{seq}
    ## Delete item api
    It receives user(phone_number) and Authorization as Header values.
    It is deleted based on the seq number assigned to the item.
    
    ## Headers:
        user: user_phone_number
        authorization: login jwt token
    
    ## Response:
        {
            "meta": {
                "code": 200,
                "message": "ok"
                },
            "data": "success"
        }
    """
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
        raise CustomHttpException(
            500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(
            500, error=e, message="Unknown error. Contact service manager.")


@item_router.get("/{seq}")
async def get_item(seq: int, user: str = Header(None), authorization: str = Header(None)):
    """GET /item/{seq}
    ## GET item api
    It receives user(phone_number) and Authorization as Header values.
    Item information is queried through the seq number assigned to the item.
    
    ## Headers:
        user: user_phone_number
        authorization: login jwt token
    
    ## Response:
        {
            "meta": {
                "code": 200,
                "message": "ok"
                },
            "data": {
                "phone_number": phone_number,
                "category": category,
                "selling_price": selling_price,
                "cost_price": cost_price,
                "name": name,
                "description": description,
                "barcode": barcode,
                "expiration_date": expiration_date,
                "size": size
            }
        }
    """
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
        raise CustomHttpException(
            500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(
            500, error=e, message="Unknown error. Contact service manager.")


@item_router.post("/{seq}")
async def update_item(seq: int, item: UpdateItem, user: str = Header(None), authorization: str = Header(None)):
    """POST /item/{seq}
    ## Update item api
    It receives user(phone_number) and Authorization as Header values.
    It receives the item information to be modified as the body value.
    
    ## Headers:
        user: user_phone_number
        authorization: login jwt token
    
    ## Body:
        **optional params**
        category (str): item category
        selling_price (int): item selling price
        cost_price (int): item cost price
        name (str): item name
        description (str): item description
        barcode (str): item barcode
        expiration_date (str): item expiration_date **required format: 20XX-XX-XX**
        size (str): itme size **required format: small, large**

    
    ## Response:
        {
            "meta": {
                "code": 200,
                "message": "ok"
                },
            "data": {
                "phone_number": phone_number,
                "chage_value": [change_params_key, ...]
            }
        }
    """
    try:
        # check user login
        ApiValidator.check_current_user(user, authorization)
        
        # check user valid input(expriation_date, size)
        ApiValidator.check_user_valid_input(item.expiration_date, item.size)
        
        # Update user item in DB
        result = MySQLManager.update_item_info(user, seq, item.dict())
        return make_respose({"phone_number": user, "change_value": result})
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except MySQLManagerError as e:
        raise CustomHttpException(
            500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(
            500, error=e, message="Unknown error. Contact service manager.")
        

@item_router.get("/")
async def get_all_item(user: str = Header(None), authorization: str = Header(None), page_number: int = 0, keyword: str = None):
    """GET /item?page_number={page_number}&keyword={keyword}
    ## GET all item api & Get search item api
    It receives user(phone_number) and Authorization as Header values.
    There is a page_number parameter that can be viewed 10 per page.
    There is a keyword parameter to search for a specific keyword.
    
    ## Headers:
        user: user_phone_number
        authorization: login jwt token

    ## Response:
        {
            "meta": {
                "code": 200,
                "message": "ok"
                },
            "data": [{
                "phone_number": phone_number,
                "category": category,
                "selling_price": selling_price,
                "cost_price": cost_price,
                "name": name,
                "description": description,
                "barcode": barcode,
                "expiration_date": expiration_date,
                "size": size
                }, ...
            ]
        }
    """
    try:
        # check user login
        ApiValidator.check_current_user(user, authorization)
        
        # If there is no keyword, search all items
        if not keyword:
            result = MySQLManager.get_all_item(user, page_number)
        else:
            result = MySQLManager.get_search_item(user, keyword, page_number)
        return make_respose(result)
    except BadRequestError as e:
        raise CustomHttpException(400, error=e)
    except UnAuthorizationError as e:
        raise CustomHttpException(401, error=e)
    except MySQLManagerError as e:
        raise CustomHttpException(
            500, error=e, message="Try again in a few minutes.")
    except Exception as e:
        raise CustomHttpException(
            500, error=e, message="Unknown error. Contact service manager.")
        
