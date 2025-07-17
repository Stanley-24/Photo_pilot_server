# app/models/subscription.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid
from datetime import datetime, timedelta

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(64), ForeignKey("users.id"))
    plan = Column(String(255), default="free")
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscription")
