from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from post_routes import router as post_router
from middleware import process_time_middleware
from pydantic import BaseModel

app = FastAPI()

# ----------------------
# CORS Middleware
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Custom Middleware ( Imported )
# ----------------------
@app.middleware("http")
async def add_process_time(request, call_next):
    return await process_time_middleware(request, call_next)


# ----------------------
# Routes
# ----------------------
@app.get("/")
def home():
    return {"message": "Hello, World!", "status": 200}


@app.get("/{item_id}/{name}")
def get_item(item_id: int, name: str):
    return {"data": {"item_id": item_id, "name": name}, "status": 200}


@app.post("/user")
def create_user(name: str, age: int):
    return {"data": f"User created with name: {name} and age: {age}", "status": 200}


class Item(BaseModel):
    name: str
    price: float
    description: str = None


@app.post("/items")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

# Include Posts CRUD routes
app.include_router(post_router, prefix="/posts", tags=["Posts"])


# poetry run uvicorn main:app --reload
