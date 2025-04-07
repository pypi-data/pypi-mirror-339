from sqlalchemy.orm import Session
from database.models import User
from database.database import engine, SessionLocal


def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    
    if not existing_user:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    db.close()
    
    return user.state if user else None
