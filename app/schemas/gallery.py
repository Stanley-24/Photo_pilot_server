from pydantic import BaseModel
from datetime import datetime

class PhotoOut(BaseModel):
    id: str
    user_id: str
    image_url: str
    timestamp: datetime

    class Config:
        orm_mode = True
