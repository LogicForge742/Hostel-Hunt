from flask import Flask
from config import Config
# app/__init__.py
from .routes.admin import admin_bp  # your admin routes


# Import extensions
from .extensions.db import db
from .extensions.jwt import jwt
try:
    from .extensions.mail import mail
except Exception:
    mail = None

# Import blueprints
from .routes.auth import auth_bp
try:
    from .routes.hostels import bp as hostels_bp
except Exception:
    hostels_bp = None


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    try:
        jwt.init_app(app)
    except Exception:
        # JWT extension may be optional in some environments
        pass
    try:
        mail.init_app(app)
    except Exception:
        pass

    # Register blueprints
    app.register_blueprint(auth_bp)
    if hostels_bp is not None:
        app.register_blueprint(hostels_bp, url_prefix="/hostels")


    # Register admin blueprint
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
