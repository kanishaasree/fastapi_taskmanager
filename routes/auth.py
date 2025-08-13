from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database import get_session
from models import User
from authentic.utils import hash_password, verify_password, create_access_token

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_session)):
    from sqlmodel import select
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_pwd)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/token")
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    from sqlmodel import select
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
