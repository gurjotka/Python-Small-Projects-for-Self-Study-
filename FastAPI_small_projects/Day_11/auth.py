from fastapi import APIRouter, HTTPException, Depends
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_token
from database import fake_db

router = APIRouter()


# 👤 REGISTER
@router.post("/register")
def register(user: UserCreate):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="User exists")

    fake_db[user.username] = {
        "username": user.username,
        "password": hash_password(user.password),
        "role": "user"   # default role
    }

    fake_db["john"]["role"] = "admin"

    return {"message": "User created"}


# 🔐 LOGIN
@router.post("/login")
def login(user: UserLogin):
    db_user = fake_db.get(user.username)

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user.username,
        "role": db_user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}