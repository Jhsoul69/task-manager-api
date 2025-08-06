# 🧠 Task Manager API — MacV AI Software Engineer Submission

A full-featured Task & Project Management API built with **FastAPI**, **PostgreSQL**, and **Docker**. Supports secure JWT authentication, email notifications, and background job processing with Celery.

---

## 🚀 Features

- ✅ User registration & login with JWT
- ✅ CRUD for Projects & Tasks
- ✅ Assign tasks to users
- ✅ Filter, sort, and paginate tasks
- ✅ Email notifications on assignment/status update
- ✅ Celery background worker for async jobs
- ✅ PostgreSQL + SQLAlchemy + Alembic migrations
- ✅ Fully containerized with Docker & Docker Compose
- ✅ ✅ ✅ **Deployed API with public access link** ✅ ✅ ✅

---

## 🔗 🔴 Live Deployed API (Public Access)

> 🌐 **Base URL:** https://localhost:8000/ 
> 🔒 Access: All routes require JWT Bearer token (except `/register`, `/token`)  
> 📄 Docs: `https://localhost:8000/docs`

**Sample Test User:**

- Email: `testuser@example.com`  
- Password: `testpassword`

---

## ⚙️ Local Setup (with Docker)

```bash
# 1. Clone the repo
git clone <your-github-repo>
cd task-manager-api

# 2. Create .env
cp .env.example .env

# 3. Start the containers
docker-compose up --build -d

# 4. Run database migration
docker-compose exec web alembic upgrade head

