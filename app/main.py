from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from . import models, database
from .auth import router as auth_router
from .routers import projects, tasks

# ✅ Load .env variables
load_dotenv()

# ✅ Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# ✅ Create FastAPI app
app = FastAPI(
    title="MacV Task Manager API",
    description="A lightweight task/project management system built with FastAPI",
    version="1.0.0",
)

# ✅ CORS FIX for Railway: allow specific domain OR allow "*"
origins = [
    "https://task-manager-api-production.up.railway.app",  # ✅ Your deployed frontend/API domain
    "http://localhost",
    "http://localhost:8000",
    "*",  # 👈 KEEP THIS ONLY FOR DEVELOPMENT!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


