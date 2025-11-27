"""
Lesson 14: Building a Simple REST API with Flask
------------------------------------------------
Goal: expose your own API endpoints so other programs can interact with them.

Prerequisites
-------------
1. Install Flask once: `python3 -m pip install flask`.
2. Optional: install `httpie` or use `curl` for easy testing.

Step-by-step walkthrough
------------------------
1. Import Flask and create an `app`.
2. Define in-memory data (a tiny task list) for demonstration purposes.
3. Build CRUD endpoints:
   - GET /tasks         -> list tasks
   - POST /tasks        -> create task
   - PATCH /tasks/<id>  -> toggle completion
   - DELETE /tasks/<id> -> delete task
4. Run the development server and test with curl or a REST client.
"""

from __future__ import annotations

from typing import Dict, List

try:
    from flask import Flask, jsonify, request
except ImportError:  # pragma: no cover - instructional guard
    Flask = None  # type: ignore[assignment]
    jsonify = request = None  # type: ignore[assignment]
else:
    Flask = Flask  # type: ignore[assignment]


if Flask:
    app = Flask(__name__)

    tasks: List[Dict[str, object]] = [
        {"id": 1, "title": "Learn Python basics", "completed": True},
        {"id": 2, "title": "Call an external API", "completed": False},
    ]
    next_task_id = 3

    def _find_task(task_id: int) -> Dict[str, object] | None:
        """Helper to locate a task by id."""
        return next((task for task in tasks if task["id"] == task_id), None)

    @app.get("/tasks")
    def list_tasks():
        """Return all tasks."""
        return jsonify(tasks)

    @app.post("/tasks")
    def create_task():
        """Create a new task from JSON payload."""
        global next_task_id
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")

        if not title:
            return jsonify({"error": "title is required"}), 400

        task = {"id": next_task_id, "title": title, "completed": False}
        tasks.append(task)
        next_task_id += 1
        return jsonify(task), 201

    @app.patch("/tasks/<int:task_id>")
    def toggle_task(task_id: int):
        """Toggle completion status."""
        task = _find_task(task_id)
        if not task:
            return jsonify({"error": "task not found"}), 404

        task["completed"] = not task["completed"]
        return jsonify(task)

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        """Delete a task by id."""
        task = _find_task(task_id)
        if not task:
            return jsonify({"error": "task not found"}), 404

        tasks.remove(task)
        return "", 204
else:
    app = None


def print_instructions() -> None:
    """Print step-by-step testing instructions."""
    print(
        "Step-by-step\n"
        "1) Install Flask: python3 -m pip install flask\n"
        "2) Run this file: python3 lessons/14_flask_api.py\n"
        "3) In another terminal, test endpoints:\n"
        "   - curl http://127.0.0.1:5000/tasks\n"
        '   - curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" '
        "-d '{\"title\":\"Build an API\"}'\n"
        "   - curl -X PATCH http://127.0.0.1:5000/tasks/2\n"
        "   - curl -X DELETE http://127.0.0.1:5000/tasks/1\n"
        "4) Inspect the JSON responses in your terminal.\n"
    )


if __name__ == "__main__":
    if not Flask or app is None:
        print("Flask is required for this lesson.")
        print_instructions()
    else:
        print_instructions()
        app.run(debug=True, port=5000)

# --- Your turn --------------------------------------------------------------
# 1. Add a PUT /tasks/<id> endpoint to edit task titles.
# 2. Validate that titles are at least 3 characters long.
# 3. Replace the in-memory list with file or database storage.
# 4. Add pagination or filtering (e.g., /tasks?completed=true).

