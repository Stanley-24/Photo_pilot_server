from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies import get_current_user
from app.routes.auth import User
from pathlib import Path
from uuid import uuid4
from PIL import Image, ImageEnhance
import os
from app.database import get_db

from sqlalchemy.orm import Session
from app.models.photo import Photo
from datetime import datetime
import shutil



router = APIRouter()

ENHANCED_DIR = "app/uploads/enhanced"
os.makedirs(ENHANCED_DIR, exist_ok=True)





@router.get("/enhance-photo")
def enhance_photo(filename: str, user: User = Depends(get_current_user)):
    image_path = Path(f"app/uploads/photos/{filename}")
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        img = Image.open(image_path)

        # Brightness and contrast enhancement
        img = ImageEnhance.Brightness(img).enhance(1.15)
        img = ImageEnhance.Contrast(img).enhance(1.2)
        img = ImageEnhance.Sharpness(img).enhance(1.3)

        # Save preview
        preview_name = f"enhanced-{uuid4()}.png"
        preview_path = Path(ENHANCED_DIR) / preview_name
        img.save(preview_path)

        return {
            "msg": "Enhancement complete",
            "preview_url": f"/uploads/enhanced/{preview_name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")




@router.post("/save-enhanced")
def save_enhanced_image(
    filename: str = Query(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enhanced_path = Path(f"app/uploads/enhanced/{filename}")
    if not enhanced_path.exists():
        raise HTTPException(status_code=404, detail="Enhanced image not found")

    new_filename = f"enhanced-{uuid4()}.png"
    replaced_path = Path("app/uploads/replaced") / new_filename

    try:
        shutil.copy(enhanced_path, replaced_path)

        # Save to DB
        photo = Photo(
            user_id=user.id,
            image_url=f"/uploads/replaced/{new_filename}",
            timestamp=datetime.utcnow()
        )
        db.add(photo)
        db.commit()

        return {
            "msg": "Enhanced image saved to gallery",
            "url": f"/uploads/replaced/{new_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Saving failed: {str(e)}")




