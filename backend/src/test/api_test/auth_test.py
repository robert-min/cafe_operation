import pytest
from enum import Enum
from httpx import AsyncClient
from lib.db_connect import MySQLManager
from api import create_app


class Mock(Enum):
    """Mock data for testing"""
    PHONE_NUMBER = "010-0000-0000"
    PASSWORD = "12312312"

app = create_app()
MySQLManager = MySQLManager()

@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_signup_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    
    
@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Clean Mock data on db after testing."""
    def remove_test_data():
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)

    request.addfinalizer(remove_test_data)
