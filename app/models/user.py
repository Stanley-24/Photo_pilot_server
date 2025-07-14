from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)  # ✅ ADD THIS
    name = Column(String)
    # ✅ Relationship
    image_tags = relationship("ImageTag", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
