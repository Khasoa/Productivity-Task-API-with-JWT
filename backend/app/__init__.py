from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import Config

# Instantiate extensions outside create_app so models can import them cleanly
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(test_config=None):
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow test overrides (e.g. in-memory SQLite)
    if test_config:
        app.config.update(test_config)

    # Bind extensions to this app instance
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register all routes
    from app.routes import register_routes
    register_routes(app)

    return app