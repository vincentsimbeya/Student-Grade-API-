from typing import List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date
import logging

# ---------------------------
# App setup
# ---------------------------
app = FastAPI(
    title="Student Grades & Tasks API",
    version="1.0.0",
    description="A simple REST API for managing student grades and tasks"
)

# Enable CORS so React (port 3003) can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)

# ---------------------------
# In-memory storage
# ---------------------------
grades_db: dict[int, list[dict]] = {}   # student_id → list of grades
grade_counter = 1                       # auto-increment grade IDs
tasks: dict[int, dict] = {}             # task_id → task data

# ---------------------------
# Grade Models
# ---------------------------
class GradeCreate(BaseModel):
    course: str = Field(..., min_length=2, max_length=50, example="Software Engineering")
    score: float = Field(..., ge=0, le=100, example=78.5)
    semester: Literal["Semester 1", "Semester 2"]
    due_date: date = Field(..., example="2026-05-20")

class Grade(GradeCreate):
    grade_id: int

class GradesResponse(BaseModel):
    student_id: int
    grades: List[Grade]

class AverageResponse(BaseModel):
    student_id: int
    average: float

class ErrorResponse(BaseModel):
    detail: str

# ---------------------------
# Task Models
# ---------------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    tags: List[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    tags: List[str] = []

# ---------------------------
# Custom validation handler
# ---------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )

# ---------------------------
# Grade Endpoints
# ---------------------------
@app.post("/students/{student_id}/grades", response_model=Grade)
def add_grade(student_id: int, grade: GradeCreate):
    """Add a grade for a student."""
    global grade_counter
    grade_id = grade_counter
    grade_counter += 1
    if student_id not in grades_db:
        grades_db[student_id] = []
    new_grade = grade.dict()
    new_grade["grade_id"] = grade_id
    grades_db[student_id].append(new_grade)
    logging.info(f"Added grade for student {student_id}: {new_grade}")
    return new_grade

@app.get("/students/{student_id}/grades", response_model=GradesResponse)
def get_student_grades(student_id: int):
    """Get all grades for a student."""
    if student_id not in grades_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student_id": student_id, "grades": grades_db[student_id]}

@app.get("/students/{student_id}/average", response_model=AverageResponse)
def get_student_average(student_id: int):
    """Get the average score for a student."""
    if student_id not in grades_db or not grades_db[student_id]:
        raise HTTPException(status_code=404, detail="No grades found")
    avg = sum(g["score"] for g in grades_db[student_id]) / len(grades_db[student_id])
    logging.info(f"Average for student {student_id}: {avg}")
    return {"student_id": student_id, "average": avg}

@app.delete("/students/{student_id}/grades/{grade_id}", response_model=ErrorResponse)
def delete_grade(student_id: int, grade_id: int):
    """Delete a grade by ID for a student."""
    if student_id not in grades_db:
        raise HTTPException(status_code=404, detail="Student not found")
    grades = grades_db[student_id]
    for g in grades:
        if g["grade_id"] == grade_id:
            grades.remove(g)
            logging.info(f"Deleted grade {grade_id} for student {student_id}")
            return {"detail": "Grade deleted"}
    raise HTTPException(status_code=404, detail="Grade not found")

# ---------------------------
# Task Endpoints
# ---------------------------
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    """Create a new task with optional tags."""
    task_id = len(tasks) + 1
    tasks[task_id] = task.dict()
    tasks[task_id]["id"] = task_id
    logging.info(f"Created task {task_id}: {tasks[task_id]}")
    return tasks[task_id]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Retrieve a task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task (title, description, tags)."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_update.dict(exclude_unset=True).items():
        tasks[task_id][field] = value
    logging.info(f"Updated task {task_id}: {tasks[task_id]}")
    return tasks[task_id]

@app.delete("/tasks/{task_id}", response_model=ErrorResponse)
def delete_task(task_id: int):
    """Delete a task by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    logging.info(f"Deleted task {task_id}")
    return {"detail": "Task deleted"}
