from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from src.auth.utils import register_user, authenticate_user, create_access_token, refresh_access_token
from src.db.client import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
# from src.auth.models import UserCreate
from src.db.schemas import UserCreate

from src.db.models import User
from src.auth.models import Token
from src.auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS, REFRESH_TOKEN_EXPIRE_MINUTES
from src.auth.auth import get_current_user
router = APIRouter(prefix="/auth", tags=["Auth"])


## AUTH
@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    await register_user(db, user) #type: ignore
    return {"message": "User registered"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token({"sub": user.username}, timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS))
    # refresh_token = create_access_token({"sub": user.username}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/refresh")
def refresh_token(refresh_token: str = Header(...)):
    try:
        new_access = refresh_access_token(refresh_token)
        return {"access_token": new_access}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# @router.get("/protected")
# async def protected_route(current_user=Depends(get_current_user)):
#     return {"message": f"Welcome {current_user.username}!"}


@router.get("/check")
async def check_auth(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}