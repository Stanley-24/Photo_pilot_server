from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from PIL import Image
import requests
from io import BytesIO
import uuid
import os
import shutil

from rembg import remove
from urllib.parse import unquote


from datetime import datetime

from app.database import get_db
from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.schemas.gallery import PhotoOut
from app.routes.auth import get_current_user




from app.dependencies import get_current_user
from app.utils.unsplash_helper import get_unsplash_backgrounds

router = APIRouter()

@router.get("/background-suggestions")
def background_suggestions(
    query: str = "nature",
    user_id: str = Depends(get_current_user)
):
    try:
        backgrounds = get_unsplash_backgrounds(query=query)
        return {"backgrounds": backgrounds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unsplash error: {str(e)}")





@router.post("/preview-replace-bg")
async def preview_replace_bg(
    file: UploadFile = File(...),
    background_url: str = Form(...),
    user_id: str = Depends(get_current_user)
):
    try:
        # Read original image
        contents = await file.read()
        removed_bg = remove(contents)
        user_image = Image.open(BytesIO(removed_bg)).convert("RGBA")

        # Download background
        response = requests.get(background_url)
        response.raise_for_status()
        bg_image = Image.open(BytesIO(response.content)).convert("RGBA")

        # Resize to match
        bg_image = bg_image.resize(user_image.size)

        # Composite
        final = Image.alpha_composite(bg_image, user_image)

        # Save to a temp preview folder
        preview_dir = "app/uploads/previews"
        os.makedirs(preview_dir, exist_ok=True)
        filename = f"preview-{uuid.uuid4()}.png"
        path = os.path.join(preview_dir, filename)
        final.save(path)

        return {
            "preview_url": f"/uploads/previews/{filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")
    
    



@router.post("/save-replaced")
def save_replaced_image(
    filename: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # Construct full paths
    previews_dir = os.path.join("app", "uploads", "previews")
    replaced_dir = os.path.join("app", "uploads", "replaced")
    os.makedirs(replaced_dir, exist_ok=True)

    source_path = os.path.join(previews_dir, filename)

    if not os.path.exists(source_path):
        raise HTTPException(status_code=404, detail="Replaced image not found")

    # Generate unique filename for saved image
    new_filename = f"replaced-{uuid.uuid4()}.png"
    dest_path = os.path.join(replaced_dir, new_filename)

    # Move the file
    shutil.move(source_path, dest_path)

    # Save to DB
    new_photo = Photo(user_id=user_id, image_url=f"/uploads/replaced/{new_filename}")
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return {
        "msg": "Image saved to gallery",
        "url": new_photo.image_url
    }