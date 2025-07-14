# app/crud/tag.py

from app.models.image_tag import ImageTag
import uuid

def save_image_tag(db, user_id, image_name, tags):
    for tag in tags:
        db.add(ImageTag(
            id=str(uuid.uuid4()),
            tag=tag["label"],  # ✅ FIXED
            user_id=user_id,
            image_name=image_name
        ))
    db.commit()
