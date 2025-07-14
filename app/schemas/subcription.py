# app/schemas/subscription.py
from pydantic import BaseModel
from datetime import datetime

class SubscriptionRead(BaseModel):
    plan: str
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True  # replaces orm_mode
