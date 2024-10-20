import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.models.users import User
from api.models.token import TokenData
from .passw_utils import PasswordUtils
from .db_utils import get_session

load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session: Session, email: str) -> User | None:
    """
    Get user
    :param session: DB Session
    :param email: email of the user
    :return: User details Or None
    """
    return session.exec(select(User).where(User.email == email)).first()


def authenticate_user(session: Session, email: str, password: str) -> bool:
    """
    Authenticate user
    :param session: DB Session
    :param email: Email of user
    :param password: Password of user
    :return: True if user exists else False
    """
    user = get_user(session, email)
    if not user or not PasswordUtils(passw=password).verify_passw():
        return False
    return True


def generate_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate token to be sent on successful authentication
    :param data: data to be added on token
    :param expires_delta: Expiration time in days
    :return: token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    Get the current user info based on token
    This function is also used to validate the token.
    :param token: access token
    :param session: DB Session
    :return: User
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(session, token_data.email)
    if not user:
        raise credentials_exception
    return user
