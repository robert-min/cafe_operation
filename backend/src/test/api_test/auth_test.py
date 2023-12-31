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
    # Error: 잘못된 전화번호 양식
    error_case = ["010", "010-0000000", "0100-0000-0000"]
    for case in error_case:
        async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
            resp = await ac.post("/auth/signup", json={
                "phone_number": case,
                "password": Mock.PASSWORD.value
            })
        assert resp.status_code == 400
        assert resp.json()["meta"]["error"] == "The input does not fit the phone number format."
    
    # Success: 신규 계정 등록 성공
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["phone_number"] == Mock.PHONE_NUMBER.value
    
    # Error: 기존에 있는 계정 등록
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/signup", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 400
    assert resp.json()["meta"]["error"] == "This phone number already exists. Please log in with your existing account."
    
    
@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_user():
    # Error: 잘못된 전화번호 양식
    error_case = ["010", "010-0000000", "0100-0000-0000"]
    for case in error_case:
        async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
            resp = await ac.post("/auth/login", json={
                "phone_number": case,
                "password": Mock.PASSWORD.value
            })
        assert resp.status_code == 400
        assert resp.json()["meta"]["error"] == "The input does not fit the phone number format."
    
    # Error: 존재하지 않는 전화번호 로그인
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": "010-1555-1555",
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 400
    assert resp.json()["meta"]["error"] == "Invalid phone number. Please check your phone number."
    
    # Erorr : 잘못된 비밀번호 로그인
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": "A12312312"
        })
    assert resp.status_code == 401
    assert resp.json()["meta"]["error"] == "Wrong password. Please check your password."
    
    # Success: 로그인 성공
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        resp = await ac.post("/auth/login", json={
            "phone_number": Mock.PHONE_NUMBER.value,
            "password": Mock.PASSWORD.value
        })
    assert resp.status_code == 200
    assert resp.json()["data"]["user"] == Mock.PHONE_NUMBER.value


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Clean Mock data on db after testing."""
    def remove_test_data():
        MySQLManager.delete_user_auth(Mock.PHONE_NUMBER.value)

    request.addfinalizer(remove_test_data)
