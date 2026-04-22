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