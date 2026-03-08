from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes_skills import router as skills_router
from app.api.routes_roadmap import router as roadmap_router
from app.api.routes_interview import router as interview_router
from app.api.routes_auth import router as auth_router
from app.api.routes_progress import router as progress_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)

# API routes
app.include_router(skills_router)
app.include_router(roadmap_router)
app.include_router(interview_router)
app.include_router(auth_router)
app.include_router(progress_router)

# Serve your existing frontend
app.mount("/", StaticFiles(directory="web", html=True), name="web")