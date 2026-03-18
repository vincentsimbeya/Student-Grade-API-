from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task List API",
    version="1.0.0",
    description="A simple pre-built FastAPI task list app for Software Requirements Engineering Lab 2.",
)

# In-memory store for lab/demo purposes
# In a real application, this would be replaced with a database.
tasks_db: list[dict] = []
next_task_id = 1


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=300, description="Task description")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    completed: Optional[bool] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Task List API is running",
        "docs": "/docs",
    }


@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
def create_task(task: TaskCreate):
    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
    }
    tasks_db.append(new_task)
    next_task_id += 1
    return new_task


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int = Path(..., gt=0)):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_update: TaskUpdate, task_id: int = Path(..., gt=0)):
    for task in tasks_db:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.description is not None:
                task["description"] = task_update.description
            if task_update.completed is not None:
                task["completed"] = task_update.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int = Path(..., gt=0)):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
