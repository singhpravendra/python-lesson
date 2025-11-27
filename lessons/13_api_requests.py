"""
Lesson 13: Working with Web APIs (Client Side)
----------------------------------------------
Goal: learn how to call third-party REST APIs using Python.

Prerequisites
-------------
1. Ensure you have internet access.
2. Install the popular `requests` library once: `python3 -m pip install requests`.

Step-by-step walkthrough
------------------------
1. Import the `requests` library (handled lazily so this file can be imported
   even before you install the dependency).
2. Prepare the base URL for a sample API. We use https://jsonplaceholder.typicode.com,
   a free fake API perfect for practice.
3. Send GET requests to retrieve resources (posts, comments).
4. Send POST requests to create resources (the fake API echoes your payload).
5. Handle errors and timeouts gracefully.
6. Package the logic into reusable helper functions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


API_BASE = "https://jsonplaceholder.typicode.com"


def _import_requests():
    """
    Import requests lazily so the module can be loaded without the dependency.
    Raises a helpful message if the package is missing.
    """
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - instructional guard
        raise SystemExit(
            "Install the 'requests' package first:\n"
            "python3 -m pip install requests"
        ) from exc
    return requests


def fetch_posts(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch a limited number of posts."""
    requests = _import_requests()
    response = requests.get(f"{API_BASE}/posts", params={"_limit": limit}, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_post_comments(post_id: int) -> List[Dict[str, Any]]:
    """Fetch comments for a specific post."""
    requests = _import_requests()
    response = requests.get(f"{API_BASE}/posts/{post_id}/comments", timeout=10)
    response.raise_for_status()
    return response.json()


def create_post(title: str, body: str, user_id: int = 1) -> Dict[str, Any]:
    """Send a POST request to create a new post (the API will echo the payload)."""
    requests = _import_requests()
    payload = {"title": title, "body": body, "userId": user_id}
    response = requests.post(f"{API_BASE}/posts", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def pretty_print_post(post: Dict[str, Any]) -> None:
    """Display a post in a readable format."""
    print(f"\nPost #{post['id']} by user {post['userId']}")
    print(f"Title : {post['title']}")
    print(f"Body  : {post['body'][:60]}...")


def step_by_step_demo() -> None:
    """Run through the lesson steps with print statements."""
    print("Step 1) Fetching example posts...")
    posts = fetch_posts(limit=3)
    for post in posts:
        pretty_print_post(post)

    print("\nStep 2) Fetching comments for the first post...")
    comments = fetch_post_comments(post_id=posts[0]["id"])
    print(f"Found {len(comments)} comments. Showing the first one:")
    first_comment = comments[0]
    print(f"- Name: {first_comment['name']}")
    print(f"- Email: {first_comment['email']}")
    print(f"- Body: {first_comment['body'][:60]}...")

    print("\nStep 3) Creating a fake post via POST request...")
    created_post = create_post(
        title="Learning APIs with Python",
        body="APIs let our programs talk to other services on the web.",
    )
    print("API echo response:", created_post)

    print("\nAll steps completed successfully!")


if __name__ == "__main__":
    step_by_step_demo()

# --- Your turn --------------------------------------------------------------
# 1. Update `fetch_posts` to accept a `user_id` filter, call it, and print the results.
# 2. Add a `fetch_todos` function that calls /todos?_limit=5 and prints done vs pending.
# 3. Wrap `create_post` in try/except to print friendlier messages on network errors.
# 4. Explore another public API (e.g., https://api.agify.io) and replicate the steps.

