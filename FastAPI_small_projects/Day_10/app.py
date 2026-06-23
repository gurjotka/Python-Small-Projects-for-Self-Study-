from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_token
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



@app.get("/home")
def home():
    return {"message": "FastAPI is running 🚀"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]




@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you are inside the VIP zone 🕶️"}