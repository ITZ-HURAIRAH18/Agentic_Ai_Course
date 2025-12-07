from fastapi import FastAPI

app = FastAPI()

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




# poetry run uvicorn main:app --reload