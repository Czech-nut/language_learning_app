from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from backend.database.user import retrieve_user_by_email
from backend.dtos.user import UserOut
from backend.exceptions import Forbidden, Unauthorised
from backend.settings import Settings
from backend.utils.logging import setup_logging

setup_logging()

settings = Settings()
reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


algorithm = "HS256"
access_token_expire_minutes = 30
refresh_token_expire_minutes = 60 * 24 * 7  # 7 days
jwt_secret_key = settings.secret_key
jwt_refresh_secret_key = settings.refresh_secret_key
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=access_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=refresh_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_refresh_secret_key, algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(reusable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[algorithm])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise Unauthorised()
    except (jwt.JWTError, ValidationError):
        raise Forbidden()

    return await retrieve_user_by_email(token_data.sub)
