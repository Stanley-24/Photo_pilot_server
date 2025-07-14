# app/models/enums.py
from enum import Enum

class SubscriptionPlan(str, Enum):
    free = "free"
    pro = "pro"
    business = "business"
