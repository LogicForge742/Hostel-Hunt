from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..services.auth_service import AuthService
from ..utils.validator import is_valid_email, is_valid_password, is_valid_phone

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# --- CORS Preflight Support ---
@auth_bp.route("/register", methods=["OPTIONS"])
def register_options():
    return "", 200

@auth_bp.route("/login", methods=["OPTIONS"])
def login_options():
    return "", 200
# --------------------------------


# Register
@auth_bp.post("/register")
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    phone_number = data.get("phone_number")
    role = data.get("role", "student")  # Default to student if not provided

    # Validation
    if not email or not is_valid_email(email):
        return jsonify({"message": "Invalid email address"}), 400
    if not password or not is_valid_password(password):
        return jsonify({"message": "Password must be at least 8 characters with uppercase, lowercase, number, and special character"}), 400
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if not phone_number or not is_valid_phone(phone_number):
        return jsonify({"message": "Invalid phone number"}), 400
    if role not in ["student", "landlord"]:
        return jsonify({"message": "Invalid role"}), 400

    response, error = AuthService.register(
        email, password, name=name, phone_number=phone_number, role=role
    )
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "Registration successful", **response}), 201


# Login
@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not email or not is_valid_email(email):
        return jsonify({"message": "Invalid email address"}), 400
    if not password or not is_valid_password(password):
        return jsonify({"message": "Password must be at least 8 characters with uppercase, lowercase, number, and special character"}), 400

    response, error = AuthService.login(email, password)
    if error:
        return jsonify({"message": error}), 401

    return jsonify({"message": "Login successful", **response}), 200


# Refresh token
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), 200


# Protected Route
@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    return jsonify({"message": "Authenticated", "user_id": user_id}), 200
