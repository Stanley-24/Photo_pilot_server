# app/utils/permissions.py

from fastapi import HTTPException, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from app.routes.auth import get_current_user  # assuming you have this

# ✅ Check if subscription is active and not expired
def verify_active_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user.subscription or not user.subscription.is_active:
        raise HTTPException(status_code=403, detail="You have no active subscription.")

    if user.subscription.end_date < datetime.utcnow():
        user.subscription.is_active = False
        db.commit()
        raise HTTPException(status_code=403, detail="Your subscription has expired.")

    return user  # Return user so it can be reused in route if needed


# ✅ Check if the user is on one of the allowed plans
def check_plan(user, required: list[str]):
    if not hasattr(user, "subscription") or not user.subscription:
        raise HTTPException(status_code=403, detail="You are on the free plan. Please upgrade.")
    
    if user.subscription.plan not in required:
        raise HTTPException(status_code=403, detail="Upgrade your plan to access this feature.")
