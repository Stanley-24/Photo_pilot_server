from rembg import remove
from PIL import Image
from io import BytesIO

def replace_background(foreground_bytes: bytes, background_bytes: bytes) -> BytesIO:
    fg_no_bg = remove(foreground_bytes)  # Remove background
    fg_img = Image.open(BytesIO(fg_no_bg)).convert("RGBA")
    bg_img = Image.open(BytesIO(background_bytes)).convert("RGBA")

    # Resize background to match foreground
    bg_resized = bg_img.resize(fg_img.size)

    # Composite foreground over background
    final_img = Image.alpha_composite(bg_resized, fg_img)

    output_buffer = BytesIO()
    final_img.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer
