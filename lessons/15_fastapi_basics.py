"""
Lesson 15: Building REST APIs with FastAPI
-------------------------------------------
FastAPI is a modern, fast web framework for building APIs with Python.
It provides automatic API documentation, type validation, and async support.

Prerequisites
-------------
1. Install FastAPI and Uvicorn: `python3 -m pip install fastapi uvicorn`
2. Optional: install `httpie` or use `curl` for testing

Step-by-step walkthrough
------------------------
1. Import FastAPI and create an app instance
2. Define Pydantic models for request/response validation
3. Create in-memory data storage
4. Build CRUD endpoints with automatic documentation
5. Run the server with Uvicorn
6. Test endpoints and view automatic API docs
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime

# Step 1: Create FastAPI app instance
app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built with FastAPI",
    version="1.0.0"
)

# Step 2: Define Pydantic models for data validation
class TaskBase(BaseModel):
    """Base model for task data."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass

class TaskUpdate(BaseModel):
    """Model for updating a task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """Model for task response (includes id and timestamps)."""
    id: int
    completed: bool
    created_at: datetime

    class Config:
        """Pydantic config for example values in docs."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Learn FastAPI",
                "description": "Build a REST API with FastAPI",
                "completed": False,
                "created_at": "2024-01-15T10:30:00"
            }
        }

# Step 3: In-memory data storage (in production, use a database)
tasks_db: List[dict] = [
    {
        "id": 1,
        "title": "Learn Python basics",
        "description": "Complete Python fundamentals course",
        "completed": True,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "title": "Build a REST API",
        "description": "Create an API using FastAPI",
        "completed": False,
        "created_at": datetime.now()
    }
]
next_id = 3

def _find_task(task_id: int) -> Optional[dict]:
    """Helper function to find a task by ID."""
    return next((task for task in tasks_db if task["id"] == task_id), None)

# Step 4: Define API endpoints

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to Task Manager API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
def list_tasks(completed: Optional[bool] = None):
    """
    Get all tasks.
    
    - **completed**: Optional filter by completion status (true/false)
    - Returns list of all tasks matching the filter
    """
    if completed is None:
        return tasks_db
    return [task for task in tasks_db if task["completed"] == completed]

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int):
    """
    Get a specific task by ID.
    
    - **task_id**: The ID of the task to retrieve
    - Returns the task if found, 404 if not found
    """
    task = _find_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-200 characters)
    - **description**: Optional task description (max 1000 characters)
    - Returns the created task with generated ID
    """
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "created_at": datetime.now()
    }
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update an existing task.
    
    - **task_id**: The ID of the task to update
    - **title**: Optional new title
    - **description**: Optional new description
    - **completed**: Optional completion status
    - Returns the updated task
    """
    task = _find_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update only provided fields
    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.description is not None:
        task["description"] = task_update.description
    if task_update.completed is not None:
        task["completed"] = task_update.completed
    
    return task

@app.patch("/tasks/{task_id}/toggle", response_model=TaskResponse, tags=["Tasks"])
def toggle_task(task_id: int):
    """
    Toggle the completion status of a task.
    
    - **task_id**: The ID of the task to toggle
    - Returns the updated task
    """
    task = _find_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    task["completed"] = not task["completed"]
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int):
    """
    Delete a task by ID.
    
    - **task_id**: The ID of the task to delete
    - Returns 204 No Content on success, 404 if not found
    """
    task = _find_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    tasks_db.remove(task)
    return None

def print_instructions():
    """Print step-by-step instructions for running and testing the API."""
    print("\n" + "="*60)
    print("FastAPI Task Manager - Step-by-Step Instructions")
    print("="*60)
    print("\nStep 1: Install dependencies")
    print("  python3 -m pip install fastapi uvicorn")
    print("\nStep 2: Run the server")
    print("  python3 lessons/15_fastapi_basics.py")
    print("  OR")
    print("  uvicorn lessons.15_fastapi_basics:app --reload")
    print("\nStep 3: View automatic API documentation")
    print("  Open your browser and visit:")
    print("  - Swagger UI: http://127.0.0.1:8000/docs")
    print("  - ReDoc: http://127.0.0.1:8000/redoc")
    print("\nStep 4: Test endpoints (in another terminal)")
    print("  # Get all tasks")
    print("  curl http://127.0.0.1:8000/tasks")
    print("\n  # Get only completed tasks")
    print("  curl http://127.0.0.1:8000/tasks?completed=true")
    print("\n  # Create a new task")
    print('  curl -X POST http://127.0.0.1:8000/tasks \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"title": "Learn FastAPI", "description": "Master API development"}\'')
    print("\n  # Update a task")
    print('  curl -X PUT http://127.0.0.1:8000/tasks/1 \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"title": "Updated title", "completed": true}\'')
    print("\n  # Toggle task completion")
    print("  curl -X PATCH http://127.0.0.1:8000/tasks/2/toggle")
    print("\n  # Delete a task")
    print("  curl -X DELETE http://127.0.0.1:8000/tasks/1")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print_instructions()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# --- Your turn --------------------------------------------------------------
# 1. Add a GET /tasks/stats endpoint that returns count of completed vs pending tasks.
# 2. Add query parameters to /tasks for pagination (limit, offset).
# 3. Add a POST /tasks/{task_id}/duplicate endpoint to clone a task.
# 4. Add request validation to ensure title is not empty.
# 5. Replace in-memory storage with a JSON file (use lesson 8 file handling).
# 6. Add tags/categories to tasks and filter by tag.

