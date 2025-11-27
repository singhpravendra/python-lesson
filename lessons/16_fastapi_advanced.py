"""
Lesson 16: Advanced FastAPI Features
------------------------------------
Learn advanced FastAPI concepts: async/await, dependencies, middleware,
authentication, and background tasks.

Prerequisites
-------------
1. Complete Lesson 15 (FastAPI Basics)
2. Install: `python3 -m pip install fastapi uvicorn python-multipart`
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Header, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime
import time

app = FastAPI(title="Advanced FastAPI Features", version="2.0.0")

# Enable CORS (Cross-Origin Resource Sharing) for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 1: Dependencies - Reusable functions for common logic
def get_api_key(api_key: str = Header(..., description="API key for authentication")):
    """
    Dependency function for API key authentication.
    In production, validate against a database or environment variable.
    """
    valid_keys = ["secret-key-123", "admin-key-456"]  # Example keys
    if api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

def get_pagination_params(skip: int = 0, limit: int = 10):
    """Dependency for pagination parameters."""
    if limit > 100:
        limit = 100  # Max limit
    if skip < 0:
        skip = 0
    return {"skip": skip, "limit": limit}

# Step 2: Pydantic Models
class User(BaseModel):
    """User model."""
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class UserCreate(BaseModel):
    """Model for creating a user."""
    name: str
    email: EmailStr

class Message(BaseModel):
    """Message model for background tasks."""
    recipient: str
    content: str

# Step 3: In-memory storage
users_db: List[dict] = []
next_user_id = 1

# Step 4: Background Tasks
def send_email_notification(message: Message):
    """
    Simulate sending an email (background task).
    In production, this would call an email service.
    """
    print(f"[BACKGROUND TASK] Sending email to {message.recipient}")
    print(f"[BACKGROUND TASK] Content: {message.content}")
    time.sleep(1)  # Simulate email sending delay
    print(f"[BACKGROUND TASK] Email sent successfully!")

def log_user_creation(user_id: int, user_name: str):
    """Log user creation in background."""
    print(f"[LOG] User {user_id} ({user_name}) created at {datetime.now()}")

# Step 5: Middleware Example
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Step 6: Async Endpoints
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint demonstrating async."""
    return {
        "message": "Advanced FastAPI API",
        "features": [
            "Dependencies",
            "Background Tasks",
            "Middleware",
            "Async/Await",
            "Authentication"
        ]
    }

@app.post("/users", response_model=User, status_code=201, tags=["Users"])
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    """
    Create a new user with background tasks.
    
    Requires API key authentication via header:
    - Header: api-key: secret-key-123
    
    Background tasks:
    - Sends welcome email
    - Logs user creation
    """
    global next_user_id
    
    # Check if email already exists
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    next_user_id += 1
    
    # Add background tasks
    background_tasks.add_task(
        send_email_notification,
        Message(recipient=user.email, content=f"Welcome {user.name}!")
    )
    background_tasks.add_task(log_user_creation, new_user["id"], user.name)
    
    return new_user

@app.get("/users", response_model=List[User], tags=["Users"])
async def list_users(
    pagination: dict = Depends(get_pagination_params),
    api_key: str = Depends(get_api_key)
):
    """
    List all users with pagination.
    
    Query parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 10, max: 100)
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    return users_db[skip:skip + limit]

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(
    user_id: int,
    api_key: str = Depends(get_api_key)
):
    """Get a specific user by ID."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Step 7: Dependency with sub-dependencies
def get_current_user(api_key: str = Depends(get_api_key)) -> dict:
    """Get current user from API key (simplified example)."""
    # In production, decode JWT or query database
    return {"id": 1, "name": "Admin", "email": "admin@example.com"}

@app.get("/profile", tags=["Users"])
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile (requires authentication)."""
    return {
        "message": "Your profile",
        "user": current_user
    }

# Step 8: Request/Response Models
class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    uptime_seconds: float

start_time = time.time()

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        uptime_seconds=time.time() - start_time
    )

def print_instructions():
    """Print step-by-step instructions."""
    print("\n" + "="*60)
    print("Advanced FastAPI Features - Instructions")
    print("="*60)
    print("\nStep 1: Install dependencies")
    print("  python3 -m pip install fastapi uvicorn python-multipart")
    print("\nStep 2: Run the server")
    print("  python3 lessons/16_fastapi_advanced.py")
    print("\nStep 3: Test with authentication")
    print("  # Create a user (requires API key)")
    print('  curl -X POST http://127.0.0.1:8000/users \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -H "api-key: secret-key-123" \\')
    print('    -d \'{"name": "Alice", "email": "alice@example.com"}\'')
    print("\n  # List users with pagination")
    print("  curl -H 'api-key: secret-key-123' http://127.0.0.1:8000/users?skip=0&limit=5")
    print("\n  # Get user profile")
    print("  curl -H 'api-key: secret-key-123' http://127.0.0.1:8000/profile")
    print("\n  # Health check (no auth required)")
    print("  curl http://127.0.0.1:8000/health")
    print("\nStep 4: View API documentation")
    print("  http://127.0.0.1:8000/docs")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print_instructions()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# --- Your turn --------------------------------------------------------------
# 1. Implement JWT token authentication instead of API keys.
# 2. Add rate limiting middleware to prevent abuse.
# 3. Create a database connection dependency using SQLAlchemy.
# 4. Add request logging middleware that writes to a file.
# 5. Implement WebSocket endpoints for real-time features.
# 6. Add file upload endpoint using File and UploadFile.
# 7. Create a dependency that validates user permissions.

