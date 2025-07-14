from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_user, UserRead
from app.schemas.review import ReviewCreate, ReviewRead
from app.models.review import Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewRead)
def submit_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    new_review = Review(
        photo_id=review.photo_id,
        comment=review.comment,
        rating=review.rating,
        user_id=current_user.id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
