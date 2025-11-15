from flask_jwt_extended import jwt_required
from app.middleware.auth_middleware import admin_required
from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.get("/dashboard")
@jwt_required()
@admin_required
def dashboard():
    return jsonify({"message": "Welcome Admin"})
