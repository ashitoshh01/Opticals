from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, name: str, email: str, password: str, phone: Optional[str] = None) -> User:
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        phone=phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
