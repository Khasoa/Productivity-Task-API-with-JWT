"""
FocusFlow API test suite.
Covers: auth flow, protected routes, CRUD, ownership, pagination.

Run with: pytest tests/ -v
"""
import pytest
from app import create_app, db


# ──────────────────────────────────────────
# FIXTURES
# ──────────────────────────────────────────

@pytest.fixture
def app():
    """
    Create a test app using an in-memory SQLite DB.
    Each test gets a fresh database — no state bleeds between tests.
    """
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-jwt-secret",
    })

    with test_app.app_context():
        db.create_all()       # Build tables
        yield test_app
        db.session.remove()
        db.drop_all()         # Tear down after each test


@pytest.fixture
def client(app):
    """HTTP test client."""
    return app.test_client()


@pytest.fixture
def auth(client):
    """
    Helper that registers a user and returns their JWT token.
    Usage: token = auth("alice", "pass123")
    Makes it easy to create multiple users in ownership tests.
    """
    def _auth(username="alice", password="pass123"):
        client.post("/signup", json={"username": username, "password": password})
        res = client.post("/login", json={"username": username, "password": password})
        return res.get_json()["access_token"]
    return _auth


@pytest.fixture
def headers(auth):
    """
    Pre-built Authorization header for the default user (alice).
    Keeps individual tests clean — no repeated token setup.
    """
    token = auth()
    return {"Authorization": f"Bearer {token}"}


# ──────────────────────────────────────────
# AUTH TESTS
# ──────────────────────────────────────────

class TestSignup:
    """Rubric: Signup (10 pts) + Model & Password (10 pts)"""

    def test_signup_success(self, client):
        """Valid signup returns 201 and a JWT token."""
        res = client.post("/signup", json={
            "username": "lydia",
            "password": "securepass"
        })
        data = res.get_json()

        assert res.status_code == 201
        assert "access_token" in data          # Logged in immediately
        assert data["user"]["username"] == "lydia"
        assert "password" not in data["user"]  # Password hash never exposed

    def test_signup_duplicate_username(self, client):
        """Duplicate username returns 400 — unique constraint enforced."""
        client.post("/signup", json={"username": "lydia", "password": "pass1"})
        res = client.post("/signup", json={"username": "lydia", "password": "pass2"})

        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_signup_missing_fields(self, client):
        """Missing username or password returns 400."""
        res = client.post("/signup", json={"username": "lydia"})  # No password
        assert res.status_code == 400


class TestLogin:
    """Rubric: Login (10 pts)"""

    def test_login_success(self, client):
        """Correct credentials return 200 with an access token."""
        client.post("/signup", json={"username": "lydia", "password": "pass123"})
        res = client.post("/login", json={"username": "lydia", "password": "pass123"})
        data = res.get_json()

        assert res.status_code == 200
        assert "access_token" in data

    def test_login_wrong_password(self, client):
        """Wrong password returns 401 — not 403 or 404."""
        client.post("/signup", json={"username": "lydia", "password": "pass123"})
        res = client.post("/login", json={"username": "lydia", "password": "wrongpass"})

        assert res.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Username that doesn't exist returns 401."""
        res = client.post("/login", json={"username": "ghost", "password": "pass123"})
        assert res.status_code == 401


class TestMe:
    """Rubric: Check Session / Me (10 pts)"""

    def test_me_authenticated(self, client, headers):
        """Valid token returns the current user's profile."""
        res = client.get("/me", headers=headers)
        data = res.get_json()

        assert res.status_code == 200
        assert data["username"] == "alice"    # Matches the auth fixture default
        assert "password_hash" not in data    # Sensitive field never exposed

    def test_me_no_token(self, client):
        """
        Request with no token returns 401.
        This is what 'stays logged in on refresh' tests in JWT:
        if the token is gone (e.g. cleared from storage), the user is logged out.
        """
        res = client.get("/me")
        assert res.status_code == 401

    def test_me_invalid_token(self, client):
        """Tampered or expired token is rejected."""
        res = client.get("/me", headers={"Authorization": "Bearer notarealtoken"})
        assert res.status_code == 422  # Flask-JWT-Extended returns 422 for malformed tokens


# ──────────────────────────────────────────
# TASK TESTS
# ──────────────────────────────────────────

class TestTaskCRUD:
    """Rubric: Resource CRUD Routes and Pagination (10 pts)"""

    def test_create_task(self, client, headers):
        """POST /tasks creates a task and returns 201."""
        res = client.post("/tasks", json={
            "title": "Finish capstone",
            "description": "Due Friday",
            "priority": "High"
        }, headers=headers)
        data = res.get_json()

        assert res.status_code == 201
        assert data["title"] == "Finish capstone"
        assert data["priority"] == "High"
        assert data["completed"] is False      # Default value

    def test_create_task_no_title(self, client, headers):
        """Missing title returns 400 — not a silent 500."""
        res = client.post("/tasks", json={"description": "No title here"}, headers=headers)
        assert res.status_code == 400

    def test_get_tasks(self, client, headers):
        """GET /tasks returns the user's tasks with pagination keys."""
        client.post("/tasks", json={"title": "Task 1"}, headers=headers)
        client.post("/tasks", json={"title": "Task 2"}, headers=headers)

        res = client.get("/tasks", headers=headers)
        data = res.get_json()

        assert res.status_code == 200
        assert len(data["tasks"]) == 2
        # Pagination keys must be present (rubric requirement)
        assert "page" in data
        assert "total_pages" in data
        assert "total_tasks" in data

    def test_pagination(self, client, headers):
        """Page 2 returns a different (or empty) set of tasks."""
        # Create 6 tasks — per_page is 5, so page 2 should have 1
        for i in range(6):
            client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

        page1 = client.get("/tasks?page=1", headers=headers).get_json()
        page2 = client.get("/tasks?page=2", headers=headers).get_json()

        assert len(page1["tasks"]) == 5
        assert len(page2["tasks"]) == 1
        assert page1["total_pages"] == 2

    def test_get_single_task(self, client, headers):
        """GET /tasks/:id returns the specific task."""
        created = client.post("/tasks", json={"title": "Solo task"}, headers=headers).get_json()
        res = client.get(f"/tasks/{created['id']}", headers=headers)

        assert res.status_code == 200
        assert res.get_json()["title"] == "Solo task"

    def test_update_task(self, client, headers):
        """PATCH /tasks/:id updates only the sent fields."""
        task = client.post("/tasks", json={"title": "Old title"}, headers=headers).get_json()

        res = client.patch(f"/tasks/{task['id']}", json={
            "title": "New title",
            "completed": True
        }, headers=headers)
        data = res.get_json()

        assert res.status_code == 200
        assert data["title"] == "New title"
        assert data["completed"] is True

    def test_delete_task(self, client, headers):
        """DELETE /tasks/:id removes the task — subsequent GET returns 404."""
        task = client.post("/tasks", json={"title": "Delete me"}, headers=headers).get_json()

        del_res = client.delete(f"/tasks/{task['id']}", headers=headers)
        assert del_res.status_code == 200

        get_res = client.get(f"/tasks/{task['id']}", headers=headers)
        assert get_res.status_code == 404


# ──────────────────────────────────────────
# OWNERSHIP + PROTECTION TESTS
# ──────────────────────────────────────────

class TestOwnershipAndProtection:
    """
    Rubric: Protected Routes (10 pts)
    The most important security tests — users cannot touch each other's data.
    """

    def test_unauthenticated_cannot_access_tasks(self, client):
        """No token = 401 on all task endpoints."""
        assert client.get("/tasks").status_code == 401
        assert client.post("/tasks", json={"title": "x"}).status_code == 401
        assert client.patch("/tasks/1", json={}).status_code == 401
        assert client.delete("/tasks/1").status_code == 401

    def test_user_cannot_read_other_users_tasks(self, client, auth):
        """
        Alice creates a task. Bob cannot see it in his task list.
        This tests the user_id filter in GET /tasks.
        """
        alice_headers = {"Authorization": f"Bearer {auth('alice', 'pass1')}"}
        bob_headers = {"Authorization": f"Bearer {auth('bob', 'pass2')}"}

        # Alice creates a task
        client.post("/tasks", json={"title": "Alice's secret task"}, headers=alice_headers)

        # Bob's task list should be empty
        bob_tasks = client.get("/tasks", headers=bob_headers).get_json()["tasks"]
        assert len(bob_tasks) == 0

    def test_user_cannot_update_other_users_task(self, client, auth):
        """Bob cannot PATCH Alice's task — should get 404 (not 403)."""
        alice_headers = {"Authorization": f"Bearer {auth('alice', 'pass1')}"}
        bob_headers = {"Authorization": f"Bearer {auth('bob', 'pass2')}"}

        alice_task = client.post(
            "/tasks", json={"title": "Alice's task"}, headers=alice_headers
        ).get_json()

        res = client.patch(
            f"/tasks/{alice_task['id']}",
            json={"title": "Hacked"},
            headers=bob_headers
        )
        # 404 (not 403) — we don't confirm the resource exists to unauthorized users
        assert res.status_code == 404

    def test_user_cannot_delete_other_users_task(self, client, auth):
        """Bob cannot DELETE Alice's task."""
        alice_headers = {"Authorization": f"Bearer {auth('alice', 'pass1')}"}
        bob_headers = {"Authorization": f"Bearer {auth('bob', 'pass2')}"}

        alice_task = client.post(
            "/tasks", json={"title": "Don't delete me"}, headers=alice_headers
        ).get_json()

        res = client.delete(f"/tasks/{alice_task['id']}", headers=bob_headers)
        assert res.status_code == 404

        # Task should still exist for Alice
        alice_res = client.get(f"/tasks/{alice_task['id']}", headers=alice_headers)
        assert alice_res.status_code == 200