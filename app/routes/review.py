from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_user, UserRead
from app.schemas.review import ReviewCreate, ReviewRead, HomepageReviewCreate, HomepageReviewRead
from app.models.review import Review
from typing import Optional
from app.models.homepage_review import HomepageReview

router = APIRouter(tags=["Reviews"])

# New endpoint for homepage reviews
@router.post("/homepage", response_model=HomepageReviewRead, tags=["Homepage Reviews"])
def submit_homepage_review(
    review: HomepageReviewCreate,
    db: Session = Depends(get_db)
):
    homepage_review = HomepageReview(
        full_name=review.full_name,
        review=review.review,
        star=review.star,
        avatar_url=review.avatar_url
    )
    db.add(homepage_review)
    db.commit()
    db.refresh(homepage_review)
    return homepage_review

@router.get("/homepage", response_model=list[HomepageReviewRead], tags=["Homepage Reviews"])
def get_homepage_reviews(db: Session = Depends(get_db)):
    return db.query(HomepageReview).order_by(HomepageReview.created_at.desc()).all()

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
