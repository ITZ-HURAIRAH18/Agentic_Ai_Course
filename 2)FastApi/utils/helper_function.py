from datetime import datetime, timedelta
from multiprocessing import context
from typing import Optional
from dotenv import load_dotenv
import jwt
import os
from passlib.context import CryptContext
# Load .env variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
print(f"Loaded SECRET_KEY: {SECRET_KEY}")
print(f"Loaded ALGORITHM: {ALGORITHM}")
print(f"Loaded ACCESS_TOKEN_EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})

        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token

    except Exception as e:
        print("JWT Error:", e)
        return None


# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
#         if decoded_token:
#             return decoded_token
#         else:
#             return HTTPException(status_code=401, detail="Token not parseable")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except Exception as e:
#         print('An exception occurred')
#         print(e)
#         return HTTPException(status_code=401, detail="Invalid token")
    
    
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)

def hash_password(password):
    return pwd_context.hash(password[:72])
