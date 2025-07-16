from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models import User
from src.db.client import get_async_session
from src.db.schemas import UserCreate
from src.auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS, REFRESH_TOKEN_EXPIRE_MINUTES 
from src.auth.auth import get_current_user

from loguru import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def refresh_access_token(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    new_access = create_access_token({"sub": username}, timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS))
    return new_access

async def authenticate_user(session: AsyncSession, username: str, password: str):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def register_user(session: AsyncSession, user_data: UserCreate):
    result = await session.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.plain_password)
    )
    session.add(new_user)
    await session.commit()
    return new_user


async def change_user_credentials(
    new_credentials: UserCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Check if new username is taken by someone else
    result = await session.execute(
        select(User).where(User.username == new_credentials.username)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Username already exists.")

    # Get the current user from DB to update
    result = await session.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Update fields
    user.username = new_credentials.username
    user.hashed_password = get_password_hash(new_credentials.plain_password)

    # Commit changes
    await session.commit()
    await session.refresh(user)

    return user
