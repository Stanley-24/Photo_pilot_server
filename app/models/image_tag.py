# app/models/image_tag.py
from app.models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class ImageTag(Base):
    __tablename__ = "image_tags"

    id = Column(String, primary_key=True)
    tag = Column(String, nullable=False)  # Singular 'tag', not 'tags'
    image_name = Column(String)  # if you're tracking filenames
    photo_id = Column(String, ForeignKey("photos.id"))
    user_id = Column(String, ForeignKey("users.id"))

    photo = relationship("Photo", back_populates="image_tags")
    user = relationship("User", back_populates="image_tags")
