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


class HomepageReviewCreate(BaseModel):
    full_name: str
    review: str
    star: int
    avatar_url: Optional[str] = None

class HomepageReviewRead(BaseModel):
    id: str
    full_name: str
    review: str
    star: int
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


