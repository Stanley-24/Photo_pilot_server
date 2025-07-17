from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import declarative_base, relationship  # Added relationship import
from uuid import uuid4
from datetime import datetime

from app.models.base import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(64), nullable=False)
    image_url = Column(String(255), nullable=False)  # ✅ This must exist
    timestamp = Column(DateTime, default=datetime.utcnow)
    view_count = Column(Integer, default=0)
    total_view_time = Column(Integer, default=0)
    tags = Column(JSON)  
    image_tags = relationship("ImageTag", back_populates="photo")
    reviews = relationship("Review", back_populates="photo", cascade="all, delete")



from app.models.image_tag import ImageTag
