from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.client import get_async_session
from src.db.models import User
from src.db.schemas import UserCreate, UserRead, UserUpdate
from src.auth.utils import register_user, change_user_credentials
from src.auth.auth import get_current_user

router = APIRouter(prefix="/db",tags=["Db"])


### PSQL DATABASE ENDPOINTS

@router.get("/users/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/users/create_user", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Controlla se username già esiste
    new_user = await register_user(session=session, user_data=user) # type:ignore
    return UserRead(username=new_user.username, id=new_user.id)


@router.put("/users/{user_id}", response_model=UserRead)
async def update_my_credentials(
    new_credentials: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await change_user_credentials(
        new_credentials=new_credentials,
        session=session,
        current_user=current_user,
    )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User non trovato")
    await session.delete(user)
    await session.commit()
    return {"detail": "Utente eliminato"}