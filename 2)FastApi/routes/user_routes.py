import token
from config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.todo_model import Todos, Users
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from utils.helper_function import create_access_token, hash_password, verify_password

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
class LoginRequest(BaseModel):
    email: str
    password: str
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

user_router = APIRouter()

@user_router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_hash_password=hash_password(user.password)
        print(f"Registering user with hashed password: {user_hash_password}")
        print("Orignal password:", user.password)
        new_user = Users(
            name=user.name,
            email=user.email,
            password=user_hash_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "User created successfully",
            "data": new_user
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@user_router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Get user by email
        user = db.query(Users).filter(Users.email == request.email).first()

        # If user not found or password does not match
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Create token with id, name, email
        token_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

        token = create_access_token(data=token_data)

        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "token": token
        }

        return {
            "status": "success",
            "message": "Login successful",
            "data": {"user": user_data}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
