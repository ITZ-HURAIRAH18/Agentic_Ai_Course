from fastapi import FastAPI
from post_routes import router as post_router
app = FastAPI()

@app.get("/")
def read_root():
    try:
        return {
            "data": "Hello, World!",
            "status": 200,
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
        }

@app.get("/{item_id}/{name}")
def read_root(item_id: int, name: str):
    try:
        return {
            "data": {
                "item_id": item_id,
                "name": name
            },
            "status": 200,
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
        }

@app.post("/user")
def read_root(name: str, age: int):
    try:
        return {
            "data": "User created with name: {} and age: {}".format(name, age),
            "status": 200,
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": 500,
        }
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

app.include_router(post_router,prefix="/posts", tags=["Posts"])


# poetry run uvicorn main:app --reload