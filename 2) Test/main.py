from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.post("/")
def read_root():
    return {"Hello": "Post"}
@app.delete("/")
def read_root():
    return {"Hello": "Delete"}




# poetry run uvicorn main:app --reload