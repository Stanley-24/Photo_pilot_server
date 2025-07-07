from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.utils.jwt import get_current_user, create_access_token # ✅ Import the official function


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
