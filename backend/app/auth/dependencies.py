from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.dependencies import get_db
from app.models.user import User

# OAuth2 scheme that tells FastAPI to expect a Bearer token
# in the Authorization header of incoming requests.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:

    # Decode the JWT token and validate its signature
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    # Triggered if token is malformed, expired, or tampered with
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Retrieve the user from the database
    user = db.query(User).filter(User.id == int(user_id)).first()

    # If user does not exist in DB
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Prevent inactive or suspended users from accessing protected routes
   if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user