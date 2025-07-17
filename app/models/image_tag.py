# app/models/image_tag.py
from app.models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class ImageTag(Base):
    __tablename__ = "image_tags"

    id = Column(String(64), primary_key=True)
    tag = Column(String(255), nullable=False)  # Singular 'tag', not 'tags'
    image_name = Column(String(255))  # if you're tracking filenames
    photo_id = Column(String(64), ForeignKey("photos.id"))
    user_id = Column(String(64), ForeignKey("users.id"))

    photo = relationship("Photo", back_populates="image_tags")
    user = relationship("User", back_populates="image_tags")
