from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import UserPreview, UserBasic
class ReviewCreate(BaseModel):
    photo_id: str
    comment: str
    rating: Optional[int] = None

class ReviewRead(BaseModel):
    id: str
    photo_id: str
    comment: str
    rating: Optional[int]
    created_at: datetime
    user_id: str
    user: UserBasic

    class Config:
        from_attributes = True  # replaces orm_mode


