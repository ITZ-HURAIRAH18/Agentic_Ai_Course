from datetime import datetime, timedelta
from fastapi import status
from http.client import HTTPException
from multiprocessing import context
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
import jwt
import os
from passlib.context import CryptContext
# Load .env variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
API_KEY_NAME = "x-api-key"
# print(f"Loaded SECRET_KEY: {SECRET_KEY}")
# print(f"Loaded ALGORITHM: {ALGORITHM}")
# print(f"Loaded ACCESS_TOKEN_EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT token with user info and expiration
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        print("JWT Error:", e)
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Make sure it contains id, name, email
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
def verify_api_key(api_key_header: str = Depends(api_key_header)):
    try:
        # query api keys table to check if api key exists and is active, and userid match the one in the token
        # db_api_key = get_api_key(userId)
        if api_key_header == os.getenv("API_KEY"):
            return api_key_header
        else:
            raise HTTPException(status_code=401, detail="Invalid API Key")
    except Exception as e:
      print('An exception occurred',e)
      raise HTTPException(status_code=401, detail="Invalid API Key")