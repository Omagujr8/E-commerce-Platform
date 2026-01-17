from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str, hashed: str ) -> str:
    return pwd_context.hash(plain, hashed)

def verify_password(plain: str, hashed: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain, hashed, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta |None = None):
    to_encode = data.copy()
    expire =  datetime.utcnow() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm= settings.JWT_ALGORITHM
    )
