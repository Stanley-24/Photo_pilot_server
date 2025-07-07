from app.models.image import UserImage

@router.get("/my-images", response_model=list[str])
def get_user_images(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    images = db.query(UserImage).filter(UserImage.user_id == user_id).all()
    return [img.image_url for img in images]
