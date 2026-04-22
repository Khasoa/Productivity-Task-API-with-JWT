# Productivity Task API

A secure RESTful Flask API for managing personal tasks. Users register, authenticate via JWT, and perform full CRUD operations on their own tasks — with no access to other users' data.

---

## Tech Stack

- Python 3.8 · Flask 2.2 · Flask-SQLAlchemy · Flask-Migrate
- Flask-Bcrypt (password hashing) · Flask-JWT-Extended (authentication)
- Marshmallow (serialization) · Faker (seed data) · Pytest

---

## Installation

**1. Clone the repo and navigate to the backend folder:**
```bash
git clone 
cd /backend
```

**2. Create and activate the virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root:**
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
Generate secure values with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Setup

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python seed.py
```

---

## Running the Server

```bash
flask run
# or
python run.py
```

Server runs at `http://localhost:5555`

---

## API Endpoints

### Auth

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/signup` | No | Register a new user. Returns user + JWT token |
| POST | `/login` | No | Login with credentials. Returns user + JWT token |
| GET | `/me` | Yes | Returns the currently authenticated user's profile |

**Signup / Login request body:**
```json
{ "username": "your_username", "password": "your_password" }
```

**Authenticated requests** require this header:
Authorization: Bearer <your_token>

---

### Tasks

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/tasks` | Yes | Get all tasks for the logged-in user (paginated) |
| GET | `/tasks/<id>` | Yes | Get a single task by ID |
| POST | `/tasks` | Yes | Create a new task |
| PATCH | `/tasks/<id>` | Yes | Update an existing task |
| DELETE | `/tasks/<id>` | Yes | Delete a task |

**Pagination:** `GET /tasks?page=1` — returns 5 tasks per page with `page`, `total_pages`, and `total_tasks` in the response.

**Create / Update request body:**
```json
{
  "title": "Finish report",
  "description": "Q3 summary doc",
  "priority": "High",
  "completed": false
}
```
`priority` accepts: `Low`, `Medium`, `High` (defaults to `Medium`)

---

## Security Notes

- Passwords are hashed with bcrypt — never stored in plaintext
- JWT tokens are required for all task endpoints
- Users can only view or modify their own tasks — ownership is enforced server-side via the JWT identity, not the request body
- Unauthorized access to another user's task returns `404`, not `403`, to avoid confirming resource existence

---

## Running Tests

```bash
pytest tests/ -v
```

Tests cover: signup, login, `/me` auth check, full task CRUD, pagination, and cross-user ownership protection.

---

## Seed Data

```bash
python seed.py
```

Creates 3 users with 5 tasks each. Password for all seeded users: `password123`

## Author

Lydia Khasoa

## License

For educational use and portfolio demonstration.