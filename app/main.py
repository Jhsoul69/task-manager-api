from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .auth import router as auth_router
from .routers import projects, tasks

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="MacV Task Manager API",
    description="A lightweight task/project management system built with FastAPI",
    version="1.0.0",
)

# CORS (optional, for testing in frontend/postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to the MacV Task Manager API"}
