# app/utils/tagger.py
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

CANDIDATE_TAGS = [
    "portrait", "nature", "car", "dog", "cat", "animal", "person",
    "indoor", "outdoor", "sky", "sunset", "beach", "mountain", "street", "food"
]

def generate_tags(image_path: str, top_n=3, candidate_labels=CANDIDATE_TAGS):
    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(text=candidate_labels, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits = outputs.logits_per_image
    probs = logits.softmax(dim=1).detach().numpy()[0]
    top_idxs = probs.argsort()[-top_n:][::-1]
    return [{"label": candidate_labels[i], "score": float(probs[i])} for i in top_idxs]
