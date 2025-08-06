from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .. import models, schemas, database, auth
from ..workers.email_tasks import send_task_email

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify project ownership
    project = db.query(models.Project).filter(models.Project.id == task.project_id, models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    if task.assigned_to:
        send_task_email.delay(new_task.title, task.assigned_to, "Assigned")

    return new_task

@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[int] = Query(None),
    due_date: Optional[str] = Query(None),
    project_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.Task).join(models.Project).filter(models.Project.owner_id == current_user.id)

    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if due_date:
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            query = query.filter(models.Task.due_date == due_date_obj)
        except:
            raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")
    if project_id:
        query = query.filter(models.Task.project_id == project_id)

    if sort_by == "priority":
        query = query.order_by(models.Task.priority)
    elif sort_by == "due_date":
        query = query.order_by(models.Task.due_date)

    return query.offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if assigned_to or status changed
    status_changed = task.status != task_update.status
    assignee_changed = task.assigned_to != task_update.assigned_to

    for key, value in task_update.dict().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    if assignee_changed or status_changed:
        send_task_email.delay(task.title, task.assigned_to, task.status)

    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

