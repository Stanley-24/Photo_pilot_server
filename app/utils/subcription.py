
from datetime import datetime, timedelta
from app.models.subcription import Subscription
from sqlalchemy.orm import Session
from app.models.user import User

def validate_and_update_subscription_status(subscription: Subscription, db: Session):
    """Deactivate expired subscriptions."""
    if subscription and subscription.end_date and subscription.end_date < datetime.utcnow():
        if subscription.is_active:  # Only update if currently active
            subscription.is_active = False
            db.commit()
    return subscription


def upgrade_user_subscription(user: User, plan: str, db: Session):
    now = datetime.utcnow()
    end = now + timedelta(days=30)

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




PLAN_PRICES = {
    "free": 0,
    "pro": 4500,
    "business": 12000
}


def get_plan_by_amount(amount: int):
    for plan, price in PLAN_PRICES.items():
        if price == amount:
            return plan
    return None