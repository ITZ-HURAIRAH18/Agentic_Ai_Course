
# post_routes.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    author: str = "Anonymous"


posts_db = []  # Temporary in-memory DB


# CREATE
@router.post("/")
def create_post(post: Post):
    posts_db.append(post)
    return {"message": "Post created", "data": post}


# READ ALL
@router.get("/")
def get_all_posts():
    return {"total": len(posts_db), "posts": posts_db}


# READ ONE
@router.get("/{post_id}")
def get_post(post_id: int):
    try:
        return posts_db[post_id]
    except:
        return {"error": "Post not found"}


# UPDATE
@router.put("/{post_id}")
def update_post(post_id: int, post: Post):
    try:
        posts_db[post_id] = post
        return {"message": "Post updated", "data": post}
    except:
        return {"error": "Post not found"}


# DELETE
@router.delete("/{post_id}")
def delete_post(post_id: int):
    try:
        deleted = posts_db.pop(post_id)
        return {"message": "Post deleted", "deleted": deleted}
    except:
        return {"error": "Post not found"}
