from fastapi import Depends, HTTPException, status
from jose import jwt
from app.core.config import settings


def require_admin(token: str = Depends()):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )