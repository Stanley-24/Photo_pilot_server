from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from rembg import remove
from app.dependencies import get_current_user, get_db
from uuid import uuid4
import shutil
import os

router = APIRouter()

# Directory to store background-removed images
OUTPUT_DIR = "app/uploads/removed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/remove-background")
async def remove_background(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG or PNG files are supported.")

    # Save original file temporarily
    ext = file.filename.split('.')[-1]
    input_path = f"{uuid4()}.{ext}"
    input_full_path = os.path.join(OUTPUT_DIR, f"original-{input_path}")

    with open(input_full_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Open and process image
    with open(input_full_path, "rb") as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)  # 🔥 background removed

    # Save output image
    output_filename = f"removed-{uuid4()}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(output_path, "wb") as out_file:
        out_file.write(output_data)

    # Return public URL
    public_url = f"/uploads/removed/{output_filename}"
    return {"url": public_url}
