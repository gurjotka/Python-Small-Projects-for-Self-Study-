
from fastapi import(
    FastAPI,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine
from models import Base, User
from dependencies import get_db
from pydantic import BaseModel


app = FastAPI()

# Startup event

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

# GET users

@app.get("/users")
async def get_users(
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User)
    )

    users = result.scalars().all()
    return users

# Create User
@app.post("/users")
async def create_user(
        db: AsyncSession = Depends(get_db)
):

    user = User(
        username="gurjot",
        email="gurjot@email.com"
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return user


# Get User by ID
@app.get("/users/{id}")
async def get_user(
        id: int,
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# Put Update User
class UserUpdate(BaseModel):
    username: str
    email: str

@app.put("/users/{id}")
async def update_user(id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.id == id))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not Found"
        )
    user.username = user_data.username
    user.email = user_data.email

    await db.commit()
    await db.refresh(user)

    return user


@app.delete("/users/{id}")
async def delete_user(id:int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await db.delete(user)

    await db.commit()

    return {
        "message": "User deleted successfully"
    }