from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/signup")
def signup_user():
    return "Hello"

