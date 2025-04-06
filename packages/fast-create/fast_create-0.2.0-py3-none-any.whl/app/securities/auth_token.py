from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuration
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Not used unless explicitly passed
DEFAULT_TOKEN_EXPIRATION_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenData(BaseModel):
    username: str | None = None



    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    if "sub" not in to_encode:
        raise ValueError("The 'sub' field (username) must be included in the data.")
    print(f"Access token expiration: {expire}")  # Debugging
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def refresh_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a refreshed JWT access token.
    Defaults to 35 days if no expires_delta is provided.
    """
    to_encode = data.copy()
    
    # Default to 35 days expiration for refresh tokens
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=35))
    to_encode.update({"exp": expire})
    
    # Ensure the "sub" claim (subject) is included
    if "sub" not in to_encode:
        raise ValueError("The 'sub' field (username) must be included in the data.")
    
    # Debugging expiration
    print(f"Creating refresh token with expiration: {expire} UTC")
    
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt







def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError as e:
        print(f"Token verification error: {str(e)}")
        raise credentials_exception