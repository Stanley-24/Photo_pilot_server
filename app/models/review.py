# app/models/review.py
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
import uuid

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    comment = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=True)
    photo_id = Column(String(64), ForeignKey("photos.id"), nullable=False)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    photo = relationship("Photo", back_populates="reviews")