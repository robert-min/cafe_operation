import pytest
from enum import Enum
from httpx import AsyncClient
from sqlalchemy import select
from api import create_app
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


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_setting():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value

    global authorization
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    authorization = resp.json()["data"]["token"]


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_insert_item():
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.post("/item", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        }, json={
            "category": Mock.CATEGORY.value,
            "selling_price": Mock.SELLING_PRICE.value,
            "cost_price": Mock.COST_PRICE.value,
            "name": Mock.NAME.value,
            "description": Mock.DESCRIPTION.value,
            "barcode": Mock.BARCODE.value,
            "expiration_date": Mock.EXPIRATION_DATE.value,
            "size": Mock.SIZE.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    assert resp.json()["data"]["name"] == Mock.NAME.value


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_get_item():
    global seq
    seq = MySQLManager.get_item_seq(Mock.PHONE_NUMBER.value, Mock.NAME.value)

    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.get(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    assert resp.json()["data"]["category"] == Mock.CATEGORY.value
    assert resp.json()["data"]["expiration_date"] == Mock.EXPIRATION_DATE.value


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_update_item():
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


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_delete_item():
    async with AsyncClient(app=app, base_url="http://localhost:8000", follow_redirects=True) as ac:
        resp = await ac.delete(f"/item/{seq}", headers={
            "user": Mock.PHONE_NUMBER.value,
            "Authorization": authorization
        })
    assert resp.status_code == 200
    assert resp.json()["data"] == "success"


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Clean Mock data on db after testing."""
    def remove_test_data():
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)

    request.addfinalizer(remove_test_data)
