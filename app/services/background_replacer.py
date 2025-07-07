# app/services/background_replacer.py

from PIL import Image
import uuid
import os

def replace_background(foreground_path: str, background_path: str) -> str:
    fg = Image.open(foreground_path).convert("RGBA")
    bg = Image.open(background_path).convert("RGBA")

    # Resize background to match foreground
    bg = bg.resize(fg.size)

    # Composite: place foreground on top of background
    result = Image.alpha_composite(bg, fg)

    # Save result
    output_filename = f"replaced-{uuid.uuid4()}.png"
    output_path = os.path.join("app/uploads/replaced", output_filename)
    result.save(output_path)

    return f"/uploads/replaced/{output_filename}"
