# main.py
from fastapi import FastAPI
from app.routes.gallery import router as gallery_router
from app.routes.ai_background import router as ai_background_router

from app.models.base import Base
from app.models.user import User
from app.models.photo import Photo
from app.database import engine
from fastapi.staticfiles import StaticFiles

from app.routes import background_replace

from app.routes.background_replacer import router as background_replace_router


Base.metadata.create_all(bind=engine)


from app.routes.auth import router as auth_router



app = FastAPI()


app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
app.mount("/uploads/removed", StaticFiles(directory="app/uploads/removed"), name="removed")
app.mount("/uploads/previews", StaticFiles(directory="app/uploads/previews"), name="previews")


# Register routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(gallery_router, prefix="/api/v1/gallery", tags=["Gallery"])
app.include_router(ai_background_router, prefix="/api/v1/ai", tags=["AI Backgrounds"])

app.include_router(background_replace_router, prefix="/api/v1/ai", tags=["AI Backgrounds"])

@app.get("/")
def root():
    return {"message": "PhotoPilot Backend Running ✅"}
