from app import db, bcrypt
from datetime import datetime

class User(db.Model):
    """Represents an authenticated user."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # When a user is deleted, delete all their tasks too
    tasks = db.relationship("Task", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check the password against the stored hash. Return true if it matches the stored hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Task(db.Model):
    """Represents a task created/owned by a user."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default="Medium") # Low /Medium / High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key linking this task to its owner (a User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"