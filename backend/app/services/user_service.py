from sqlalchemy.orm import Session
from app.repositories.user_repo import get_user_by_email, create_user
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate

def register_user(db: Session, user_in: UserCreate):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("User already exists")

    user = user(
        email = user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    return create_user(db, user)

