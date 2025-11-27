## FastAPI Project – Function & Method Reference

This guide explains what every function and method in the FastAPI project does, how it is used, and why it exists.

---

### `main.py`
- **`lifespan(app)`** – Async context manager fired when the FastAPI app starts and stops. Logs startup metadata (service name, env, host, port), warns when running in development mode, and announces shutdown.
- **`create_fastapi_app()`** – Factory that builds the FastAPI instance, wires CORS, request context middleware, exception handlers, health/user routers, and exposes a root `GET /` endpoint with service metadata.
- **`main()`** – Entry point. Creates the app, logs “Starting <service> on host:port,” runs Uvicorn with the configured log level/reload, and logs a matching “server stopped” message when the process exits or errors.

### `settings/config.py`
- **`Settings` (class)** – `pydantic-settings` model that loads and validates every environment variable (service info, CORS, security, logging, database). Provides helpers `is_production`/`is_development`.
- **`parse_cors_origins()`** – Normalises `CORS_ORIGINS` whether provided as CSV or list.
- **`validate_secret_key()`** – Warns if the default secret key is used in production.

### `middleware/request_context.py`
- **`RequestContextMiddleware.dispatch()`** – Runs for every request: generates or propagates `x-trace-id`, stores it in `contextvars`, times the request, injects `x-response-time-ms` and `x-trace-id` headers, and logs a concise request line containing method, path, status, duration, and client IP.

### `configs/context.py`
- **`set_trace_id(trace_id)`** – Saves the trace ID in a `ContextVar` so downstream components can read it without passing parameters.
- **`get_trace_id()`** – Retrieves the current trace ID, defaulting to `"undefined"` if none exists.

### `configs/logging_configs.py`
- **`ContextFilter.filter(record)`** – Adds `trace_id`, `service`, `env`, HTTP metadata, etc. to every log record so structured output always includes request context.
- **`get_log_format()`** – Chooses JSON or human-readable formatter based on `settings.log_format`.
- **`LOGGING_CONFIG`** – DictConfig definition consumed by `logging.config.dictConfig`, wiring formatters, handlers, and logger levels (including Uvicorn loggers).

### `exceptions/custom_exceptions.py`
- **`AppException`** – Base class carrying `message`, `status_code`, and optional `details`.
- **`NotFoundError`, `ValidationError`, `ConflictError`, `UnauthorizedError`, `ForbiddenError`** – Typed subclasses that preset HTTP status codes and messages, making it easy for services to raise meaningfully classified errors.

### `exceptions/handlers.py`
- **`setup_exception_handlers(app)`** – Registers four FastAPI exception handlers:
  - `app_exception_handler` – serialises `AppException` subclasses.
  - `validation_exception_handler` – reshapes FastAPI/Pydantic validation errors into a consistent payload.
  - `http_exception_handler` – prettifies Starlette `HTTPException` responses.
  - `general_exception_handler` – final catch-all that returns HTTP 500 with trace IDs.

### `models/user_request.py`
- **`UserCreateRequest`** – Request schema with name/email validation (length, trimming, `EmailStr`) and example payload for docs.
- **`UserUpdateRequest`** – Optional fields for partial updates; validators enforce non-empty names when provided.

### `models/user_response.py`
- **`UserResponse`** – Response schema including `id`, `name`, `email`, `created_at`, and `trace_id`.
- **`UserListResponse`** – Wraps a list of `UserResponse` plus `total` count and `trace_id` for list endpoints.

### `entities/user_entity.py`
- **`UserEntity`** – Dataclass representing a user within the domain layer; `__post_init__` stamps `created_at` when absent so repositories always store timestamps.

### `repositories/base_user_repo.py`
- **`BaseUserRepository`** – Abstract base class defining the persistence contract (`save`, `find`, `list`, `delete`). Any database implementation must satisfy this API.

### `repositories/memory_user_repo.py`
- **`save(user)`** – Stores or replaces a user in an in-memory dict.
- **`find(user_id)`** – Returns the user with matching ID or `None`.
- **`list()`** – Returns a list of all stored `UserEntity` objects.
- **`delete(user_id)`** – Removes a user entry safely (no error if missing).
- **`find_by_email(email)`** – Helper used by `UserService` to detect duplicates.

### `services/user_service.py`
- **`create(name, email)`** – Business logic for user creation: validates email, prevents duplicates (via repo), constructs `UserEntity`, persists it, and logs success.
- **`get(user_id)`** – Validates the ID and returns the user or throws `NotFoundError`.
- **`list()`** – Fetches every user and logs the count.
- **`delete(user_id)`** – Ensures the user exists before deleting, raising `NotFoundError` if not.

### `apis/routes/health.py`
- **`health()`** – `GET /api/health` basic check returning service/env/timestamp/trace ID.
- **`readiness()`** – `GET /api/health/ready` readiness probe (placeholder for DB checks, currently always ready).
- **`liveness()`** – `GET /api/health/live` liveness probe used by orchestrators.

### `apis/routes/users.py`
- **`get_user_service()`** – Dependency provider that instantiates `UserService` with an `InMemoryUserRepo`.
- **`create_user(payload, svc)`** – Validates payload via Pydantic, delegates to `UserService.create`, logs creation, returns `UserResponse`.
- **`get_user(user_id, svc)`** – Path-parameter driven fetch; produces 404 if service raises `NotFoundError`.
- **`list_users(svc)`** – Returns every user alongside a `total` count and shared trace ID.
- **`delete_user(user_id, svc)`** – Invokes `UserService.delete` and responds with HTTP 204 on success.

### `middleware/request_context.py`
- Covered above; noted separately because it’s a class with logging side effects.

### `utils/id_generator.py`
- **`generate_id()`** – Thin wrapper around `uuid.uuid4()` returning a string; used for both user IDs and trace IDs to keep ID generation consistent.

---

Use this document as a map when onboarding new contributors, writing tests, or swapping implementations (e.g., replacing the in-memory repo with a database-backed version). Each component’s responsibilities and interactions are spelled out so you can quickly trace the flow from HTTP request → router → service → repository and back. 

