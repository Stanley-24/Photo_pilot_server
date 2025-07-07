from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime

from app.models.base import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    image_url = Column(String, nullable=False)  # ✅ This must exist
    timestamp = Column(DateTime, default=datetime.utcnow)
