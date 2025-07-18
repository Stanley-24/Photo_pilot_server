# main.py
from fastapi import FastAPI
import uvicorn
from app.routes.gallery import router as gallery_router
from app.routes.ai_background import router as ai_background_router

from app.models.base import Base
from app.models.user import User
from app.models.photo import Photo
from app.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.models.subcription import Subscription

from app.routes.auth import router as auth_router
from app.routes.photo_enhancer import router as photo_enhancer_router
from app.routes.review import router as review_router
from app.routes.subcription import router as subscription_router
import os
from dotenv import load_dotenv

from starlette.middleware.sessions import SessionMiddleware  # ✅ ADD THIS

load_dotenv()
FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")

from app.routes import background_replace, tag
from app.routes.background_replacer import router as background_replace_router

print("==== FastAPI app is starting up ====", flush=True)
from app.models.base import Base
from app.models.user import User
from app.models.photo import Photo
from app.database import engine
print("==== Before Base.metadata.create_all ====", flush=True)
try:
    Base.metadata.create_all(bind=engine)
    print("==== After Base.metadata.create_all ====", flush=True)
except Exception as e:
    print(f"==== Exception in create_all: {e} ====", flush=True)
    import sys; sys.exit(1)

app = FastAPI()

# ✅ Add SessionMiddleware before including routers
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "your-default-session-secret")
)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://photo-pilot.vercel.app",
        "https://photo-pilot-client-ig515zpa6-stanley-owarietas-projects.vercel.app",
        "https://photo-pilot-client-df1nhl4pu-stanley-owarietas-projects.vercel.app",
        "https://photo-pilot-client-girkkngh1-stanley-owarietas-projects.vercel.app",
        "https://photo-pilot-client-cyrruedr8-stanley-owarietas-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Static file mounts
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
app.mount("/uploads/removed", StaticFiles(directory="app/uploads/removed"), name="removed")
app.mount("/uploads/previews", StaticFiles(directory="app/uploads/previews"), name="previews")
app.mount("/uploads/enhanced", StaticFiles(directory="app/uploads/enhanced"), name="enhanced")

# ✅ Register routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(gallery_router, prefix="/api/v1/gallery", tags=["Gallery"])
app.include_router(ai_background_router, prefix="/api/v1/ai", tags=["AI Backgrounds"])
app.include_router(background_replace_router, prefix="/api/v1/ai", tags=["AI Backgrounds"])
app.include_router(tag.router)
app.include_router(review_router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(photo_enhancer_router, prefix="/api/v1/ai", tags=["Photo Enhancer"])
app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["Subscription"])

@app.get("/")
def root():
    return {"message": "PhotoPilot Backend Running ✅"}

if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))


