# app/routes/subscription.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.dependencies import get_db
from app.models.subcription import Subscription
from app.models.user import User
from app.schemas.subcription import SubscriptionRead
from app.utils.jwt import get_current_user
from app.utils.permissions import check_plan, verify_active_subscription
from app.utils.subcription import upgrade_user_subscription
from app.utils.flutterwave import verify_flutterwave_payment

# ✅ Cleaned prefix
router = APIRouter(prefix="", tags=["Subscription"])


@router.get("/subscription/me")
def get_my_subscription(user: User = Depends(get_current_user)):
    if not user.subscription:
        return {"plan": "free", "is_active": False}

    days_remaining = (user.subscription.end_date - datetime.utcnow()).days

    return {
        "plan": user.subscription.plan,
        "is_active": user.subscription.is_active,
        "start_date": user.subscription.start_date,
        "end_date": user.subscription.end_date,
        "days_remaining": max(days_remaining, 0),
    }


@router.post("/subscription/subscribe")
def subscribe_to_plan(
    plan: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    upgrade_user_subscription(user, plan, db)
    return {"message": f"Successfully subscribed to {plan} plan!"}


@router.post("/subscription/mock-payment")
def mock_payment(
    plan: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    upgrade_user_subscription(user, plan, db)
    return {"message": f"Simulated subscription to {plan} plan!"}


@router.post("/subscription/verify-payment")
async def verify_payment(
    transaction_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    payment_data = await verify_flutterwave_payment(transaction_id)

    if not payment_data or payment_data["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment verification failed")

    amount_paid = float(payment_data["data"]["amount"])
    now = datetime.utcnow()
    end = now + timedelta(days=30)

    if amount_paid == 4500:
        plan = "pro"
    elif amount_paid == 12000:
        plan = "business"
    else:
        plan = "free"

    if user.subscription:
        user.subscription.plan = plan
        user.subscription.start_date = now
        user.subscription.end_date = end
        user.subscription.is_active = True
    else:
        new_sub = Subscription(
            user_id=user.id,
            plan=plan,
            start_date=now,
            end_date=end,
            is_active=True
        )
        db.add(new_sub)

    db.commit()
    return {"message": f"Verified and upgraded to {plan}!"}


@router.get("/subscription/advanced-feature")
def advanced_feature_access(user: User = Depends(verify_active_subscription)):
    check_plan(user, required=["pro", "premium"])  # allowed plans
    return {"message": "Welcome to the pro feature!"}
