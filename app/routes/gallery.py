# app/routes/gallery.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List
from app.database import SessionLocal
from app.models.photo import Photo
from app.utils.jwt import get_current_user
from app.schemas.gallery import PhotoOut

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
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Check MIME type (content type)
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG files are supported.")

    # Save file locally
    ext = file.filename.split('.')[-1]
    new_filename = f"{uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, new_filename)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    # Save metadata to DB
    photo = Photo(
        user_id=user_id,
        image_url=f"/uploads/photos/{new_filename}"  # 🔁 updated for public access
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo





@router.get("/me", response_model=List[PhotoOut])
def get_my_photos(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    photos = db.query(Photo).filter(Photo.user_id == user_id).all()
    return photos
