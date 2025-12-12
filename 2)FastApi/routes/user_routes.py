import token
from config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.todo_model import Todos, Users
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from utils.helper_function import create_access_token


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
        new_user = Users(
            name=user.name,
            email=user.email,
            password=user.password
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
        user = db.query(Users).filter(
            Users.email == request.email,
            Users.password == request.password
        ).first()

        # FIRST check if user exists
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # THEN create JWT token
        token = create_access_token(data={"sub": user.email})

        user_data = {
            "id": user.id,
            "email": user.email,
            "token": token
        }

        return {
            "status": "success",
            "message": "Login successful",
            "data": {"user": user_data}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
