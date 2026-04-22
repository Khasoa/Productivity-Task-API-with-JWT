from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app import db
from app.models import User, Task
from app.schemas import user_schema, task_schema, tasks_schema


def register_routes(app):
    """Register all routes on the Flask app."""

    # ──────────────────────────────────────────
    # HEALTH CHECK
    # ──────────────────────────────────────────
    @app.route("/")
    def home():
        return jsonify({"message": "FocusFlow API is running ✅"}), 200


    # ──────────────────────────────────────────
    # AUTH: SIGNUP
    # ──────────────────────────────────────────
    @app.route("/signup", methods=["POST"])
    def signup():
        """
        Register a new user.
        Body: { "username": "...", "password": "..." }
        Returns: 201 on success, 400 if validation fails
        """
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        # Validate required fields
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Enforce unique usernames (rubric requirement)
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 400

        user = User(username=username)
        user.set_password(password)  # Hashes with bcrypt

        db.session.add(user)
        db.session.commit()

        # Return the new user + a token so they're immediately logged in
        token = create_access_token(identity=user.id)
        return jsonify({
            "user": user_schema.dump(user),
            "access_token": token
        }), 201


    # ──────────────────────────────────────────
    # AUTH: LOGIN
    # ──────────────────────────────────────────
    @app.route("/login", methods=["POST"])
    def login():
        """
        Authenticate an existing user.
        Body: { "username": "...", "password": "..." }
        Returns: JWT access token on success, 401 on failure
        """
        data = request.get_json()

        user = User.query.filter_by(username=data.get("username", "")).first()

        if not user or not user.check_password(data.get("password", "")):
            # Generic message — don't reveal whether username or password was wrong
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(identity=user.id)
        return jsonify({
            "user": user_schema.dump(user),
            "access_token": token
        }), 200


    # ──────────────────────────────────────────
    # AUTH: ME (Check Session equivalent for JWT)
    # ──────────────────────────────────────────
    @app.route("/me", methods=["GET"])
    @jwt_required()
    def me():
        """
        Return the currently authenticated user's profile.
        Requires: Valid JWT in Authorization header
        Equivalent to check_session in cookie-based auth
        """
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)  # SQLAlchemy 2.x compatible

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user_schema.dump(user)), 200


    # ──────────────────────────────────────────
    # TASKS: GET ALL (with pagination)
    # ──────────────────────────────────────────
    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def get_tasks():
        """
        Fetch the logged-in user's tasks, paginated.
        Query params: ?page=1
        Returns only THIS user's tasks — ownership enforced via user_id filter
        """
        user_id = get_jwt_identity()
        page = request.args.get("page", 1, type=int)

        pagination = (
            Task.query
            .filter_by(user_id=user_id)           # ← ownership check
            .order_by(Task.created_at.desc())      # newest first
            .paginate(page=page, per_page=5, error_out=False)
        )

        return jsonify({
            "tasks": tasks_schema.dump(pagination.items),
            "page": page,
            "total_pages": pagination.pages,
            "total_tasks": pagination.total
        }), 200


    # ──────────────────────────────────────────
    # TASKS: GET ONE
    # ──────────────────────────────────────────
    @app.route("/tasks/<int:id>", methods=["GET"])
    @jwt_required()
    def get_task(id):
        """
        Fetch a single task by ID.
        Returns 404 if not found OR if it belongs to another user.
        """
        user_id = get_jwt_identity()

        # filter_by(user_id=...) is the ownership guard
        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        return jsonify(task_schema.dump(task)), 200


    # ──────────────────────────────────────────
    # TASKS: CREATE
    # ──────────────────────────────────────────
    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        """
        Create a new task for the logged-in user.
        Body: { "title": "...", "description": "...", "priority": "High" }
        user_id is set from the JWT — client cannot fake ownership
        """
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        task = Task(
            title=data["title"],
            description=data.get("description"),
            priority=data.get("priority", "Medium"),
            user_id=user_id   # Ownership set server-side, not from request body
        )

        db.session.add(task)
        db.session.commit()

        return jsonify(task_schema.dump(task)), 201


    # ──────────────────────────────────────────
    # TASKS: UPDATE
    # ──────────────────────────────────────────
    @app.route("/tasks/<int:id>", methods=["PATCH"])
    @jwt_required()
    def update_task(id):
        """
        Partially update a task.
        Only the task owner can update — enforced by user_id filter.
        """
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        data = request.get_json()

        # Only update fields that were sent — leave others unchanged
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.priority = data.get("priority", task.priority)
        task.completed = data.get("completed", task.completed)

        db.session.commit()

        return jsonify(task_schema.dump(task)), 200


    # ──────────────────────────────────────────
    # TASKS: DELETE
    # ──────────────────────────────────────────
    @app.route("/tasks/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(id):
        """
        Delete a task by ID.
        Returns 404 if not found OR if it belongs to a different user.
        """
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200