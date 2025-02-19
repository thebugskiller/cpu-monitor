from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeSerializer

from config.settings import config
from src.models import User
from src.schema import BaseUser, RegisterUser
from src.middleware.auth import get_current_user

serializer = URLSafeSerializer(config.SECRET_KEY)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register/")
async def register_user(user: RegisterUser):
    """Registers a new user with name, username and password."""
    existing_user = await User.find_one(User.username == user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=user.username,
        name=user.name,
        hashed_password=User.hash_password(user.password),
    )
    await user.insert()
    return {"message": "User registered successfully"}


@auth_router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates user and creates a session cookie."""
    user = await User.find_one(User.username == form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create a signed session token
    session_token = serializer.dumps({"user_id": str(user.id)})

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="session_id", value=session_token, httponly=True, samesite="Lax"
    )
    return response


@auth_router.get("/logout/")
async def logout():
    """Logout the user and clears the session cookie."""
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("session_id")
    return response


@auth_router.get("/profile/", response_model=BaseUser)
async def profile(user_id: str = Depends(get_current_user)):
    """Fetch user details."""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return BaseUser(name=user.name, username=user.username)
