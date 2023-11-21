import jwt
import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta

# 애플리케이션에서 사용할 시크릿 키를 설정합니다.
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"


class Token:
    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type


class UserInDB:
    def __init__(self, id: int, username: str, hashed_password: str):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password


class User:
    def __init__(self, username: str):
        self.username = username


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)
