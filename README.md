````markdown

# Productivity Task API + JWT Frontend Client

FocusFlow is a full-stack productivity project built with a Flask backend API and a React frontend client using JWT authentication. Users can create accounts, log in securely, remain authenticated across refreshes, and manage personal tasks through protected API endpoints.

This project demonstrates backend authentication, authorization, RESTful API design, frontend integration, and secure user-owned resource management.

---

## Project Structure

The repository contains two main parts: a Flask backend and a React frontend.

- `backend/` contains the Flask API, database models, tests, migrations, and seed files.
- `client-with-jwt/` contains the React frontend used for JWT authentication and future task integration.
- `README.md` is the main project guide.

---

## Features

### Authentication

Users can sign up, log in, and remain authenticated using JSON Web Tokens (JWT). Tokens are stored on the frontend and reused to maintain sessions after page refreshes.

### Task Management

Each authenticated user can manage their own tasks through secure CRUD operations.

Users can:

- Create tasks
- View all personal tasks
- View one task
- Update task details
- Delete tasks
- Access paginated task lists

### Security

Passwords are securely hashed using bcrypt and never stored in plaintext. JWT tokens are required for protected routes. Users cannot access or modify another user’s data.

---

## Tech Stack

### Backend

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Marshmallow
- Faker
- Pytest

### Frontend

- React
- JavaScript
- Fetch API
- localStorage

---

## How the Application Works

### Signup Flow

A new user submits a username and password through the React frontend. The frontend sends a request to the Flask backend. The password is hashed with bcrypt, the user is saved to the database, and a JWT token is returned.

### Login Flow

An existing user submits valid credentials. The backend verifies the stored password hash and returns a new JWT token.

### Persistent Sessions

When the frontend reloads, it checks localStorage for a saved token and sends it to the `/me` endpoint. If valid, the user remains logged in.

### Task Ownership

Whenever a task request is made, the backend extracts the logged-in user's identity from the JWT token and returns only that user's tasks.

---

## Installation Guide

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/focusflow.git
cd focusflow
````

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Create Environment Variables

Inside the `backend/` folder, create a `.env` file:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

Generate secure keys with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Setup

Run the following inside the backend folder:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python seed.py
```

This creates the database tables and inserts sample data.

---

## Running the Backend Server

```bash
flask run
```

or

```bash
python run.py
```

The backend runs locally at:

`http://localhost:5555`

---

## Running the Frontend Client

Open a new terminal and run:

```bash
cd client-with-jwt
npm install
npm start
```

The frontend runs locally at:

`http://localhost:3000`

---

## Connecting Frontend to Backend

If needed, add this line to the frontend `package.json` file:

```json
"proxy": "http://localhost:5555"
```

This allows React requests to automatically reach the Flask backend.

---

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description                       |
| ------ | -------- | --------------------------------- |
| POST   | /signup  | Register a new user               |
| POST   | /login   | Login user and receive JWT        |
| GET    | /me      | Return current authenticated user |

### Task Routes

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | /tasks?page=1 | Get paginated tasks |
| GET    | /tasks/<id>   | Get one task        |
| POST   | /tasks        | Create task         |
| PATCH  | /tasks/<id>   | Update task         |
| DELETE | /tasks/<id>   | Delete task         |

---

## Example Requests

### Signup

```json
{
  "username": "lydia",
  "password": "mypassword"
}
```

### Create Task

```json
{
  "title": "Finish project",
  "description": "Submit by Friday",
  "priority": "High"
}
```

Authenticated requests must include:

```http
Authorization: Bearer <token>
```

---

## Running Tests

Inside the backend folder:

```bash
pytest tests/ -v
```

Tests cover:

* Signup
* Login
* `/me`
* CRUD operations
* Pagination
* Unauthorized access
* Cross-user protection

---

## Seed Data

Run:

```bash
python seed.py
```

This creates:

* 3 sample users
* 5 tasks for each user

Password for all seeded users:

`password123`

---

## Why This Project Matters

This project demonstrates real-world backend engineering skills:

* Secure authentication systems
* REST API architecture
* Database relationships
* Frontend/backend integration
* Authorization logic
* Testing
* Professional project organization

---

## Author

Lydia Khasoa

---

## License

Educational use and portfolio demonstration.

```
```
