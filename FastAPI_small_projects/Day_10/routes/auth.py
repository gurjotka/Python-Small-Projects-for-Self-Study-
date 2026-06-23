from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin
from core.security import hash_password, verify_password, create_access_token

router = APIRouter()

fake_db = {}  # replace with real DB later

@router.post("/register")
def register(user: UserCreate):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User exists")

    fake_db[user.email] = {
        "email": user.email,
        "password": hash_password(user.password)
    }

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin):
    db_user = fake_db.get(user.email)

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}