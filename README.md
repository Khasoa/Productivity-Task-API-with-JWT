# Productivity Task API with JWT

A full-stack productivity project built with a Flask backend API and a React frontend client using JWT authentication. Users can register, log in securely, remain authenticated after refresh, and manage personal tasks through protected API endpoints.

This project demonstrates backend authentication, authorization, RESTful API design, frontend integration, and secure user-owned resource management.

---

## Project Structure

- `backend/` contains the Flask API, database models, routes, migrations, tests, and seed data.  
- `client-with-jwt/` contains the React frontend client.  
- `README.md` contains the full project documentation.

---

## Features

### Authentication

- User signup  
- User login  
- JWT token authentication  
- Persistent login after refresh  
- Protected routes  

### Task Management

Each user can only manage their own tasks.

- Create tasks  
- View all tasks  
- View one task  
- Update tasks  
- Delete tasks  
- Paginated task lists  

### Security

- Passwords hashed with bcrypt  
- JWT required for protected routes  
- Users cannot access another user's tasks  
- Ownership enforced server-side  

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

The frontend sends a username and password to `/signup`.  
The backend hashes the password, creates the user, generates a JWT token, and returns both the user and token.

### Login Flow

The frontend sends credentials to `/login`.  
If valid, the backend returns a JWT token.

### Persistent Sessions

The frontend stores the token in localStorage.  
On refresh, it sends the token to `/me` to keep the user logged in.

### Task Ownership

Every task request uses the JWT token identity.  
Only the logged-in user's tasks are returned.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
````

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Create Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

Generate secure values if needed:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Setup

Inside the `backend/` folder run:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python seed.py
```

This creates the database tables and inserts sample data.

---

## Running the Backend

```bash
flask run
```

or

```bash
python run.py
```

Backend URL:

```text
http://localhost:5555
```

---

## Running the Frontend

Open a new terminal:

```bash
cd client-with-jwt
npm install
npm start
```

Frontend URL:

```text
http://localhost:3000
```

---

## Connecting Frontend to Backend

If needed, add this line to the frontend `package.json`:

```json
"proxy": "http://localhost:5555"
```

---

## API Endpoints

### Authentication Routes

| Method | Endpoint  | Description            |
| ------ | --------- | ---------------------- |
| POST   | `/signup` | Register a new user    |
| POST   | `/login`  | Login user             |
| GET    | `/me`     | Get authenticated user |

### Task Routes

| Method | Endpoint        | Description         |
| ------ | --------------- | ------------------- |
| GET    | `/tasks?page=1` | Get paginated tasks |
| GET    | `/tasks/<id>`   | Get one task        |
| POST   | `/tasks`        | Create task         |
| PATCH  | `/tasks/<id>`   | Update task         |
| DELETE | `/tasks/<id>`   | Delete task         |

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

Authenticated requests require:

```http
Authorization: Bearer <token>
```

---

## Running Tests

Inside the backend folder run:

```bash
pytest tests/ -v
```

Tests cover:

* Signup
* Login
* `/me` authentication
* CRUD operations
* Pagination
* Unauthorized access
* Cross-user ownership protection

---

## Seed Data

Run:

```bash
python seed.py
```

This creates:

* 3 sample users
* 5 tasks for each user

Default password:

```text
password123
```

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

