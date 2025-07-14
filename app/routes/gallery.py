# app/routes/gallery.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Body
from sqlalchemy.orm import Session, joinedload
from uuid import uuid4
import os
from typing import List

from app.database import SessionLocal
from app.models.photo import Photo
from app.models.user import User
from app.utils.jwt import get_current_user
from app.schemas.gallery import PhotoOut
from app.utils.tagger import generate_tags  # ✅ New import for tagging
from app.models.review import Review  # Import Review model for preloading

router = APIRouter()

UPLOAD_DIR = "app/uploads/photos"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=PhotoOut)
def upload_photo(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG files are supported.")

    # Save file locally
    ext = file.filename.split('.')[-1]
    new_filename = f"{uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, new_filename)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    # ✅ Generate AI tags
    tags = generate_tags(filepath)

    # Save metadata to DB
    photo = Photo(
        user_id=user.id,
        image_url=f"/uploads/photos/{new_filename}",
        tags=tags  # ✅ Save tags
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo


@router.get("/me", response_model=List[PhotoOut])
def get_my_photos(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    photos = db.query(Photo).filter(Photo.user_id == user.id).all()
    return photos

@router.get("/photos/{photo_id}", response_model=PhotoOut)
def get_photo(photo_id: str, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # ⬇️ Increment view count
    photo.view_count += 1
    db.commit()
    db.refresh(photo)

    return photo

@router.post("/photos/{photo_id}/view", response_model=PhotoOut)
def record_view(photo_id: str, view_time: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    photo.view_count += 1
    photo.total_view_time += view_time
    db.commit()
    db.refresh(photo)

    return photo
