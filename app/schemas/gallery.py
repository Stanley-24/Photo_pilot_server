from pydantic import BaseModel
from datetime import datetime
from .review import ReviewRead
from typing import Optional, List


class PhotoOut(BaseModel):
    id: str
    user_id: str
    image_url: str
    timestamp: datetime
    view_count: int
    total_view_time: int
    reviews: Optional[List[ReviewRead]]  # ✅ PLURAL: should match the ORM relationship name

    model_config = {
        "from_attributes": True
    }
