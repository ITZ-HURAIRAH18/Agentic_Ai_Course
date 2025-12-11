from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from models.todo_model import Todos, Users
app = FastAPI()
todo_router = APIRouter()

# -------------------------
# Pydantic Model
# -------------------------
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
# -------------------------
# Create Todo
# -------------------------
@todo_router.post("/create/{user_id}")
def create_todo(user_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        new_todo = Todos(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=user_id   # <-- IMPORTANT
        )
        
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return {
            "status": "success",
            "message": "Todo created successfully",
            "data": new_todo
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -------------------------
# Get All Todos
# -------------------------
@todo_router.get("/")
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todos).all()
        return {
            "status": "success",
            "message": "Todos fetched successfully",
            "data": todos
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -------------------------
# Get Todo by ID
# -------------------------
@todo_router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {
            "status": "success",
            "message": "Todo fetched successfully",
            "data": todo
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -------------------------
# Update Todo
# -------------------------
@todo_router.put("/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        todo.title = todo_update.title
        todo.description = todo_update.description
        todo.completed = todo_update.completed

        db.commit()
        db.refresh(todo)

        return {
            "status": "success",
            "message": "Todo updated successfully",
            "data": todo
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -------------------------
# Delete Todo
# -------------------------
@todo_router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.delete(todo)
        db.commit()

        return {"status": "success", "message": "Todo deleted"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
