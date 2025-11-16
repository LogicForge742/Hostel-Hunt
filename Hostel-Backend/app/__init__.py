from flask import Flask
from config import Config
# app/__init__.py
from .routes.admin import admin_bp  # your admin routes

# Import CORS
from flask_cors import CORS

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
    from .routes.hostels import hostels_bp
except Exception:
    hostels_bp = None
try:
    from .routes.users import users_bp
except Exception:
    users_bp = None
try:
    from .routes.bookings import bookings_bp
except Exception:
    bookings_bp = None
try:
    from .routes.review import reviews_bp
except Exception:
    reviews_bp = None
try:
    from .routes.search import search_bp
except Exception:
    search_bp = None
try:
    from .routes.analytics import analytics_bp
except Exception:
    analytics_bp = None


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

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
    if users_bp is not None:
        app.register_blueprint(users_bp, url_prefix="/users")
    if bookings_bp is not None:
        app.register_blueprint(bookings_bp, url_prefix="/bookings")
    if reviews_bp is not None:
        app.register_blueprint(reviews_bp, url_prefix="/reviews")
    if search_bp is not None:
        app.register_blueprint(search_bp, url_prefix="/search")
    if analytics_bp is not None:
        app.register_blueprint(analytics_bp, url_prefix="/analytics")

    # Register admin blueprint
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
