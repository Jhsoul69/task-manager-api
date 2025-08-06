from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from . import models, database
from .auth import router as auth_router
from .routers import projects, tasks

# ✅ Load .env
load_dotenv()

# ✅ Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# ✅ Create app
app = FastAPI(
    title="MacV Task Manager API",
    description="A lightweight task/project management system built with FastAPI",
    version="1.0.0",
)

# ✅ Enable CORS for all origins (safe for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes
app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to the MacV Task Manager API"}

