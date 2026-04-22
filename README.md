# Productivity Task API + JWT Frontend Client

This is a full-stack productivity project built with a **Flask backend API** and a **React frontend client** using **JWT authentication**.

Users can create accounts, log in securely, remain authenticated across refreshes, and manage personal tasks through protected API endpoints.

This project demonstrates backend authentication, authorization, RESTful API design, frontend integration, and secure user-owned resource management.

---

## Project Structure

```bash
productivity-task-api-with-jwt/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── run.py
│   ├── seed.py
│   └── README.md
│
├── client-with-jwt/
│   ├── src/
│   └── package.json
│
└── README.md

Features

Authentication
User signup
User login
JWT token generation
Persistent login via localStorage
Protected routes using Bearer tokens
Secure password hashing with bcrypt
Task Management

Each user can manage only their own tasks.

Create tasks
View tasks
View one task
Update tasks
Delete tasks
Pagination support
Security
Passwords are never stored in plaintext
JWT required for protected routes
Users cannot access other users’ tasks
Ownership enforced server-side

Tech Stack

Backend
Python 3.8+
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Bcrypt
Flask-JWT-Extended
Marshmallow
Faker
Pytest
Frontend
React
JavaScript
Fetch API
localStorage

How It Works

Signup Flow
User submits username and password in the React frontend
Frontend sends a POST /signup request
Flask creates the user
Password is hashed with bcrypt
JWT token is generated
Token is saved in localStorage
User becomes logged in
Login Flow
User submits credentials
Frontend sends POST /login
Flask verifies password hash
JWT token is returned
Frontend stores token
Persistent Session

When the page refreshes:

Frontend reads token from localStorage
Sends GET /me
If token is valid, user remains logged in
Task Flow

Authenticated requests use:

Authorization: Bearer <token>

Backend extracts user identity from JWT and returns only that user’s tasks.

Installation Guide
1. Clone Repository
git clone https://github.com/YOUR_USERNAME/focusflow.git
cd focusflow
Backend Setup
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Create .env

Inside /backend create:

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

Generate secure values with:

python -c "import secrets; print(secrets.token_hex(32))"
Setup Database
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python seed.py
Run Backend
flask run

or

python run.py

Runs on:

http://localhost:5555
Frontend Setup

Open a new terminal:

cd client-with-jwt
npm install
npm start

Runs on:

http://localhost:3000
Connecting Frontend to Backend

If needed, add this to frontend package.json:

"proxy": "http://localhost:5555"

This allows React requests to reach the Flask API.

API Endpoints
Auth Routes
Method	Endpoint	Description
POST	/signup	Register user
POST	/login	Login user
GET	/me	Current user
Task Routes
Method	Endpoint
GET	/tasks?page=1
GET	/tasks/<id>
POST	/tasks
PATCH	/tasks/<id>
DELETE	/tasks/<id>
Example Requests
Signup
{
  "username": "lydia",
  "password": "mypassword"
}
Create Task
{
  "title": "Finish project",
  "description": "Submit by Friday",
  "priority": "High"
}
Running Tests

Inside backend:

pytest tests/ -v

Tests cover:

Signup
Login
/me
CRUD routes
Pagination
Unauthorized access
Cross-user protection
Seed Data
python seed.py

Creates:

3 users
5 tasks each

Password for seeded users:

password123
Why This Project Matters

This project demonstrates real-world backend engineering skills:

Secure authentication systems
REST API architecture
Database relationships
Frontend/backend integration
Authorization logic
Testing
Professional project organization

Author

Lydia Khasoa


License

Educational use and portfolio demonstration.