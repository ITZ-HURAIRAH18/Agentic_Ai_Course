from config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.todo_model import Todos, Users
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

user_router = APIRouter()

@user_router.post("/create_user")
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


@user_router.get("/user/{user_id}")
def get_todos_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        todos = (
            db.query(Todos)
            .options(joinedload(Todos.user))  # This loads user data along with todos
            .filter(Todos.user_id == user_id)
            .all()
        )

        data = []
        for todo in todos:
            data.append({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "user": {
                    "id": todo.user.id,
                    "name": todo.user.name,
                    "email": todo.user.email
                }
            })

        return {
            "status": "success",
            "message": f"Todos for user {user_id} fetched successfully",
            "data": data
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
