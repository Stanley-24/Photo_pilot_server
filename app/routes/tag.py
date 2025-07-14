from fastapi import APIRouter, UploadFile, File, Query, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import shutil
import os

from app.utils.tagger import generate_tags
from app.crud.tag import save_image_tag
from app.routes.auth import get_current_user, UserRead
from app.database import get_db

router = APIRouter(prefix="/tags", tags=["Image Tagging"])


@router.post("/", summary="Generate top image tags using CLIP")
async def tag_image(
    file: UploadFile = File(...),
    top_n: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        tags = generate_tags(temp_path, top_n=top_n)
        save_image_tag(db, user_id=current_user.id, image_name=file.filename, tags=tags)
        return {"image_name": file.filename, "tags": tags}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_path)




@router.post("/batch", summary="Batch tag multiple images")
async def batch_tag_images(
    files: list[UploadFile] = File(...),
    top_n: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    results = []

    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            tags = generate_tags(temp_path, top_n=top_n)
            save_image_tag(db, user_id=current_user.id, image_name=file.filename, tags=tags)
            results.append({"image_name": file.filename, "tags": tags})
        except Exception as e:
            results.append({"image_name": file.filename, "error": str(e)})
        finally:
            os.remove(temp_path)

    return {"results": results}
