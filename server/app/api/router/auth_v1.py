from fastapi import APIRouter, HTTPException, Response

from dependancies import auth_manager, get_user_crud
from ..model import UserAccountV1, UserCreateV1, UserLoginV1

router = APIRouter(
    prefix = "/v1/auth",
    tags = ["auth"],
    responses = {404: {"description": "Not found"}},
)

@router.post("/register", response_model = UserAccountV1)
def create_user(user: UserCreateV1):
    user_crud = get_user_crud()
    user = user_crud.create_user(username = user.username, email = user.email, password = user.password)
    return user

@router.post("/login", response_model = UserAccountV1)
def login_user(user: UserLoginV1):
    user_crud = get_user_crud()
    user_db = user_crud.get_user_by_email(email = user.email)
    if not user_db:
        raise HTTPException(status_code = 404, detail = "User not found")
    if not auth_manager.verify_password(password = user.password, hashed_password = user_db.hashed_password):
        raise HTTPException(status_code = 404, detail = "Incorrect password")
    token = auth_manager.create_jwt(user_id = str(user_db.id))
    response = Response()
    response.set_cookie(key = "token", value = token)
    return response