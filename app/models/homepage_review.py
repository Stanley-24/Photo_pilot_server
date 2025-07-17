from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.models.base import Base
import uuid

class HomepageReview(Base):
    __tablename__ = "homepage_reviews"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(255), nullable=False)
    review = Column(String(255), nullable=False)
    star = Column(Integer, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 