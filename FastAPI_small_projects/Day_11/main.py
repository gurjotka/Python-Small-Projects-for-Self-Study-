from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from auth import router as auth_router
from security import SECRET_KEY, ALGORITHM
from database import fake_db

app = FastAPI()

app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 👤 Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# 👤 Normal protected route
@app.get("/me")
def me(user=Depends(get_current_user)):
    return user


# 👑 ADMIN ONLY route
@app.get("/admin/dashboard")
def admin_dashboard(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only 🚫")

    return {
        "message": "Welcome Admin 👑",
        "data": "Secret admin stats here"
    }
