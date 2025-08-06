from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from . import models, database
from .auth import router as auth_router
from .routers import projects, tasks

# ✅ Load environment variables
load_dotenv()

# ✅ Create database tables (safe if already exist)
models.Base.metadata.create_all(bind=database.engine)

# ✅ Initialize FastAPI app
app = FastAPI(
    title="MacV Task Manager API",
    description="A lightweight task/project management system built with FastAPI",
    version="1.0.0",
)

# ✅ Define allowed origins explicitly
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://task-manager-api-production.up.railway.app"  # ✅ Replace if your Railway URL is different
]

# ✅ Setup CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ❌ Don't use ["*"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all routers
app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(tasks.router)

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the MacV Task Manager API"}

