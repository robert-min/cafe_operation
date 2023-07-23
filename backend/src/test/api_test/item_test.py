import jwt
import pytest
from enum import Enum
from httpx import AsyncClient
from sqlalchemy import select
from datetime import datetime, timedelta
from api import create_app
from lib import TOKEN_KEY
from lib.model import Item
from lib.db_connect import MySQLManager, MySQLManagerError


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
    EXPIRATION_DATE = "2023-08-20"
    SIZE = "small"


app = create_app()


class MySQLManager(MySQLManager):
    def __init__(self) -> None:
        super().__init__()

    def get_item_seq(self, phone_number: str, name: str) -> str:
        try:
            with self.session as session:
                sql = select(Item).filter(Item.phone_number ==
                                          phone_number, Item.name == name)
                obj = session.execute(sql).scalar_one()
            return obj.seq
        except Exception:
            raise MySQLManagerError("Failed to delete item info on DB.")


MySQLManager = MySQLManager()
authorization = ""
seq = ""
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


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_setting():
    # Create item api test account
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_required():
    # Success: 로그인 성공
    global authorization
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    authorization = resp.json()["data"]["token"]

    # Error: 본인의 토큰으로 다른사람의 API 요청
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post("/item", headers={
            "user": "010-1111-1234",
            "Authorization": authorization
        }, json=params)
    assert resp.status_code == 401
    assert resp.json()["meta"]["error"] == "The wrong approach. Go back to the previous page"
    
    # Error: 다른 유저의 토큰으로 API 요청
    wrong_token = jwt.encode({
        "phone_number": "010-1111-1234",
        "exp": datetime.utcnow() + timedelta(hours=2)
    }, TOKEN_KEY, algorithm="HS256")
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post("/item", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": wrong_token
        }, json=params)
    assert resp.status_code == 401
    assert resp.json()["meta"]["error"] == "The wrong approach. Go back to the previous page"
    
    # Error: 만료된 토큰으로 API 요청
    expired_token = jwt.encode({
        "phone_number": Mock.PHONE_NUMBER.value,
        "exp": datetime.utcnow() - timedelta(hours=2)
    }, TOKEN_KEY, algorithm="HS256")
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post("/item", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": expired_token
        }, json=params)
    assert resp.status_code == 401
    assert resp.json()["meta"]["error"] == "An expired token. Please log in again."


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_insert_item():
    # Sucess: 아이템 등록
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post("/item", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        }, json=params)
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    assert resp.json()["data"]["name"] == Mock.NAME.value

    # Sucess: 여러 아이템 등록
    for i in range(11):
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            params["name"] = Mock.NAME.value + str(i)
            resp = await ac.post("/item", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            }, json=params)
        assert resp.status_code == 200

    # Error: 잘못된 expiration_date case
    error_case = ["2024-5-12", "23-066-02", "20230522", "2023-01-9"]
    for case in error_case:
        params["expiration_date"] = case
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            params["name"] = Mock.NAME.value + str(i)
            resp = await ac.post("/item", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            }, json=params)
        assert resp.status_code == 400
        assert resp.json()["meta"]["error"] == "The input does not fit the expriation date format."
    params["expiration_date"] = Mock.EXPIRATION_DATE.value
    
    # Error: 잘못된 size case
    error_case = ["medium", "s", "l", "smaller"]
    for case in error_case:
        params["size"] = case
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
                    params["name"] = Mock.NAME.value + str(i)
                    resp = await ac.post("/item", headers={
                        "user": Mock.PHONE_NUMBER.value,
                        "Authorization": authorization
                    }, json=params)
        assert resp.status_code == 400
        assert resp.json()["meta"]["error"] == "The input does not fit the size format. (small or large)"
    params["size"] = Mock.SIZE.value

@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_get_item():
    global seq
    seq = MySQLManager.get_item_seq(Mock.PHONE_NUMBER.value, Mock.NAME.value)

    # Success : 아이템 정보 조회
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    assert resp.json()["data"]["category"] == Mock.CATEGORY.value
    assert resp.json()["data"]["expiration_date"] == Mock.EXPIRATION_DATE.value


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_update_item():
    # Success: 아이템 정보 수정
    change_value = {
        "description": "Change value",
        "barcode": "change barcode"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        }, json=change_value)
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    assert resp.json()["data"]["change_value"] == ["description", "barcode"]

    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["description"] == change_value["description"]
    assert resp.json()["data"]["barcode"] == change_value["barcode"]
    
    # Error: 잘못된 expiration_date case
    error_case = ["2024-5-12", "23-066-02", "20230522", "2023-01-9"]
    for case in error_case:
        change_value["expiration_date"] = case
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.post(f"/item/{seq}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            }, json=change_value)
            if resp.status_code == 200:
                print(case)
            assert resp.status_code == 400
            assert resp.json()["meta"]["error"] == "The input does not fit the expriation date format."
    
    # Error: 잘못된 size case
    del change_value["expiration_date"]
    error_case = ["medium", "s", "l", "smaller"]
    for case in error_case:
        change_value["size"] = case
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.post(f"/item/{seq}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            }, json=change_value)
            assert resp.status_code == 400
            assert resp.json()["meta"]["error"] == "The input does not fit the size format. (small or large)"
            
            
@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_get_all_item():
    # Success: 전체 아이템 조회
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get("/item?page_number=0", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 10
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get("/item?page_number=1", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert (len(resp.json()["data"]) > 0)
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get("/item?page_number=5", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert (len(resp.json()["data"]) == 0)


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_get_search_item():
    # Success: 검색 아이템 조회
    search_keyword = ["아메", "ㅇㅁㄹ", "아메리카", "ㅇㅁㄹㅋㄴ"]
    for keyword in search_keyword:
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.get(f"/item?page_number=0&keyword={keyword}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            })
        assert resp.status_code == 200
        assert len(resp.json()["data"]) == 10

        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.get(f"/item?page_number=1&keyword={keyword}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            })
        assert resp.status_code == 200
        assert (len(resp.json()["data"]) > 0)
    
    # Success: 존재하지 않는 데이터 검색 시 빈 리스트 조회
    keyword = "파이썬"
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.get(f"/item?page_number=0&keyword={keyword}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            })
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 0


@pytest.mark.order(8)
@pytest.mark.asyncio
async def test_delete_item():
    # single case test clean
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.delete(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert resp.json()["data"] == "success"

    # multi case test clean
    for i in range(1, 12):
        async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
            resp = await ac.delete(f"/item/{seq+i}", headers={
                "user": Mock.PHONE_NUMBER.value,
                "Authorization": authorization
            })
        assert resp.status_code == 200


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Clean Mock data on db after testing."""
    def remove_test_data():
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)

    request.addfinalizer(remove_test_data)
