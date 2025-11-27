# Production-Grade FastAPI Application

A production-ready FastAPI application with best practices, error handling, logging, and structured architecture.

## Features

- ✅ **Production-ready architecture** with clean separation of concerns
- ✅ **Comprehensive error handling** with custom exceptions
- ✅ **Structured logging** with trace IDs and context
- ✅ **Request/Response validation** using Pydantic
- ✅ **CORS middleware** for cross-origin requests
- ✅ **Health check endpoints** (health, readiness, liveness)
- ✅ **Environment-based configuration** using pydantic-settings
- ✅ **Request tracing** with trace IDs
- ✅ **Type hints** throughout the codebase
- ✅ **API documentation** (Swagger/ReDoc)
- ✅ **Monitoring hooks** via Prometheus `/metrics`

## Project Structure

```
practice/fastapi/
├── apis/
│   └── routes/          # API route handlers
│       ├── health.py    # Health check endpoints
│       └── users.py     # User CRUD endpoints
├── configs/             # Configuration modules
│   ├── context.py       # Request context (trace IDs)
│   └── logging_configs.py  # Logging configuration
├── entities/            # Domain entities
│   └── user_entity.py   # User domain model
├── exceptions/           # Custom exceptions
│   ├── custom_exceptions.py
│   └── handlers.py      # Exception handlers
├── middleware/          # Custom middleware
│   └── request_context.py  # Request context middleware
├── monitoring/          # Observability helpers
│   └── metrics.py       # Prometheus instrumentation setup
├── models/              # Pydantic models (request/response)
│   ├── user_request.py
│   └── user_response.py
├── repositories/        # Data access layer
│   ├── base_user_repo.py
│   └── memory_user_repo.py
├── services/            # Business logic layer
│   └── user_service.py
├── settings/            # Application settings
│   └── config.py        # Settings management
├── utils/               # Utility functions
│   └── id_generator.py
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## File-by-File Reference

Below is a quick guide to what each file is responsible for:

### Root Files
- `main.py` – boots the FastAPI app, wires middleware/routers, and manages startup/shutdown logging.
- `requirements.txt` – lists all runtime dependencies (FastAPI, Pydantic, etc.).
- `.env.example` – template showing every environment variable the app can consume.
- `README.md` – you are here.

### `apis/routes`
- `health.py` – exposes readiness, liveness, and general health endpoints used by load balancers/Kubernetes.
- `users.py` – REST endpoints for user CRUD; delegates to `UserService` and returns Pydantic response models.

### `configs`
- `context.py` – wraps `contextvars` so every request gets a trace ID accessible throughout the stack.
- `logging_configs.py` – centralized `logging` configuration (format, handlers, JSON vs. text output).

### `entities`
- `user_entity.py` – domain entity (dataclass) representing a user, including creation timestamp metadata.

### `exceptions`
- `custom_exceptions.py` – strongly typed application exceptions (`NotFoundError`, `ValidationError`, etc.).
- `handlers.py` – FastAPI exception handlers that convert exceptions into consistent JSON error payloads.
- `__init__.py` – re-exports the exception classes for convenient imports.

### `middleware`
- `request_context.py` – FastAPI middleware that assigns trace IDs, logs request duration, and adds headers like `x-trace-id`.

### `models`
- `user_request.py` – Pydantic request schemas (`UserCreateRequest`, `UserUpdateRequest`) with validation rules.
- `user_response.py` – Response schemas (`UserResponse`, `UserListResponse`) used by the API layer.

### `repositories`
- `base_user_repo.py` – abstract base class defining the repository contract (save, find, list, delete).
- `memory_user_repo.py` – in-memory implementation useful for demos/tests; swap with a DB-backed repo later.

### `services`
- `user_service.py` – business logic layer: validation, duplicate checks, coordination between API and repo layers.

### `settings`
- `config.py` – loads environment variables using `pydantic-settings`, enforces types, and exposes helpers like `is_production`.

### `utils`
- `id_generator.py` – singleton helper for generating UUID-based identifiers/trace IDs.

For a function-by-function walkthrough of each file, see [`docs/FUNCTIONS.md`](docs/FUNCTIONS.md).


## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# For production, set:
# - ENV=prod
# - SECRET_KEY=<strong-random-key>
# - LOG_FORMAT=json
```

### 3. Run the Application

```bash
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health
- **Prometheus Metrics**: http://localhost:8000/metrics

## Monitoring & Metrics

- The app automatically exposes Prometheus-compatible metrics at `/metrics` using `prometheus-fastapi-instrumentator`.
- To disable metrics in certain environments, set `ENABLE_METRICS=false` (instrumentation respects this env var).
- Recommended workflow:
  1. Install Prometheus and configure a scrape job pointing to your service’s `/metrics`.
  2. Use Grafana (or similar) to visualise dashboards (request rate, latency, error counts).
  3. Hook alerts to threshold queries (e.g., high `http_requests_total` error ratio).

## API Endpoints

### Health Checks

- `GET /api/health` - Basic health check
- `GET /api/health/ready` - Readiness probe (for Kubernetes)
- `GET /api/health/live` - Liveness probe (for Kubernetes)

### Users

- `POST /api/users/` - Create a new user
- `GET /api/users/` - List all users
- `GET /api/users/{user_id}` - Get user by ID
- `DELETE /api/users/{user_id}` - Delete user

## Example Requests

### Create User

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com"
  }'
```

### List Users

```bash
curl http://localhost:8000/api/users/
```

### Get User

```bash
curl http://localhost:8000/api/users/{user_id}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVICE_NAME` | Service identifier | `user-service` |
| `ENV` | Environment (dev/staging/prod) | `dev` |
| `DEBUG` | Enable debug mode | `false` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `API_PREFIX` | API URL prefix | `/api` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `*` |
| `SECRET_KEY` | Secret key for security | `change-me-in-production` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FORMAT` | Log format (json/text) | `text` |

## Production Deployment

### 1. Environment Setup

```bash
# Set production environment
export ENV=prod
export SECRET_KEY=$(openssl rand -hex 32)
export LOG_FORMAT=json
export LOG_LEVEL=INFO
```

### 2. Run with Gunicorn (Recommended)

```bash
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 3. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Kubernetes Deployment

Use the health check endpoints:
- Liveness probe: `/api/health/live`
- Readiness probe: `/api/health/ready`

## Best Practices Implemented

1. **Separation of Concerns**: Clear layers (routes → services → repositories)
2. **Error Handling**: Custom exceptions with proper HTTP status codes
3. **Logging**: Structured logging with trace IDs for request tracking
4. **Validation**: Pydantic models for request/response validation
5. **Configuration**: Environment-based settings with validation
6. **Type Safety**: Type hints throughout the codebase
7. **Documentation**: Automatic API documentation with Swagger/ReDoc
8. **Security**: CORS configuration, secret key management
9. **Observability**: Health checks, trace IDs, structured logs

## Next Steps

- [ ] Add database integration (SQLAlchemy/asyncpg)
- [ ] Implement authentication/authorization (JWT)
- [ ] Add rate limiting middleware
- [ ] Add request/response caching
- [ ] Implement pagination for list endpoints
- [ ] Add unit and integration tests
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and metrics (Prometheus)

## License

This is a learning project. Feel free to use and modify as needed.

