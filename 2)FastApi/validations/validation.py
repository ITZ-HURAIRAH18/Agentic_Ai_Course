import email
from email import message
from pydantic import BaseModel,Field,AfterValidator
from typing_extensions import Annotated


class StandardReseponse(BaseModel):
    message: str = ""
    data: list = None  # type: ignore
    status: str = ""
    # token: str 
    


class TodoCreate(BaseModel):
    title: str
    description: str = None  # type: ignore
    completed: bool = False
    # token: str 
    

class LoginUser(BaseModel):
    email: str
    password: str



def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value
class UserCreate(BaseModel):
    name: str
    email: str
    password: str