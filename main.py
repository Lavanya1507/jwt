from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import timedelta

from auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
from database import db  # MongoDB client

app = FastAPI()

# Enable CORS to allow frontend (http://localhost:3000) with cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Models -----------------
class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------- Routes -----------------

@app.post("/signup")
async def signup(user: UserSignup):
    existing_user = await db["userLoginDetails"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    await db["userLoginDetails"].insert_one({
        "email": user.email,
        "hashed_password": hashed_pw
    })

    return {"message": "User created successfully"}


@app.post("/login")
async def login(user: UserLogin):
    db_user = await db["userLoginDetails"].find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return response


@app.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response


@app.get("/dashboard")
def get_dashboard(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {current_user}!"}


@app.get("/profile")
def get_profile(current_user: str = Depends(get_current_user)):
    return {"email": current_user}


@app.get("/settings")
def get_settings(current_user: str = Depends(get_current_user)):
    return {
        "email": current_user,
        "settings": {
            "theme": "light",
            "notifications": True,
            "language": "en"
        }
    }
