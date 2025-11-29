from flask import Flask, request, jsonify
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate

from werkzeug.exceptions import HTTPException

# Import extensions
from .extensions.db import db
from .extensions.jwt import jwt
from .extensions.mail import mail

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS via flask-cors (kept) and enforce headers for all responses
    CORS(app, origins=app.config['CORS_ORIGINS'],
         methods=app.config['CORS_METHODS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

    # Ensure every response (including /auth/register landlord errors) carries CORS headers
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin:
            # Echo the calling Origin so browsers treat this as a non-wildcard CORS response
            response.headers["Access-Control-Allow-Origin"] = origin
            # Make it explicit that the response varies by Origin
            existing_vary = response.headers.get("Vary")
            if existing_vary:
                if "Origin" not in existing_vary:
                    response.headers["Vary"] = f"{existing_vary}, Origin"
            else:
                response.headers["Vary"] = "Origin"
        else:
            # Fallback for non-browser or non-CORS callers
            response.headers.setdefault("Access-Control-Allow-Origin", "*")

        response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Convert unhandled exceptions into JSON so the frontend never sees an HTML error page."""
        if isinstance(error, HTTPException):
            # Let Flask handle known HTTP exceptions (404, 401, etc.) using its default machinery
            return error

        app.logger.exception("Unhandled exception during request")
        return jsonify({"message": "Internal server error"}), 500

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints inside function to avoid circular imports
    from .routes.auth import auth_bp
    from .routes.hostels import hostels_bp
    from .routes.users import users_bp
    from .routes.bookings import bookings_bp
    from .routes.review import reviews_bp
    from .routes.search import search_bp
    from .routes.analytics import analytics_bp
    from .routes.admin import admin_bp
    from .routes.upload import upload_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(hostels_bp, url_prefix="/hostels")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(reviews_bp, url_prefix="/reviews")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(upload_bp)

    return app