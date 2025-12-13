from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from config.database import get_db
from models.todo_model import Todos
from utils.helper_function import  verify_token
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


@todo_router.post("/create")
def create_todo(todo: TodoCreate, user=Depends(verify_token), db: Session  = Depends(get_db)):
    try:
        user_id = user.get("id")  # not user_id

        db_todo = Todos(title=todo.title, description=todo.description,
                        completed=todo.completed, user_id=user_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "data": db_todo,
            "message": "Todo created successfully",
            "status": "success"
        }
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }



# -------------------------
# Get All Todos
# -------------------------
@todo_router.get("/")
def get_todos( user=Depends(verify_token),db: Session = Depends(get_db)):
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
@todo_router.get("/id/{todo_id}")
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


@todo_router.get("/user/{user_id}")
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
