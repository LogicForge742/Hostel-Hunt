from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_service import UserService
from ..utils.validator import is_valid_email, is_valid_password, is_valid_phone

users_bp = Blueprint("users", __name__, url_prefix="/users")

#CORS Preflight Support
@users_bp.route("/profile", methods=["OPTIONS"])
def profile_options():
    return "", 200

@users_bp.route("/password", methods=["OPTIONS"])
def password_options():
    return "", 200

@users_bp.route("/become-landlord", methods=["OPTIONS"])
def become_landlord_options():
    return "", 200


@users_bp.get("/profile")
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    return jsonify(user), 200

@users_bp.put("/profile")
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input data
    if 'email' in data and not is_valid_email(data['email']):
        return jsonify({"message": "Invalid email address"}), 400
    if 'phone_number' in data and not is_valid_phone(data['phone_number']):
        return jsonify({"message": "Invalid phone number"}), 400

    try:
        user = UserService.update_user_profile(user_id, data)
        return jsonify({"message": "Profile updated successfully", "user": user}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@users_bp.put("/password")
@jwt_required()
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"message": "Current password and new password are required"}), 400

    if not is_valid_password(new_password):
        return jsonify({"message": "Password must be at least 8 characters with uppercase, lowercase, number, and special character"}), 400

    try:
        UserService.change_password(user_id, current_password, new_password)
        return jsonify({"message": "Password changed successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to change password"}), 500

@users_bp.post("/become-landlord")
@jwt_required()
def become_landlord():
    """Create landlord profile for user"""
    user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['business_name', 'contact_phone', 'contact_email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if not is_valid_email(data['contact_email']):
        return jsonify({"message": "Invalid contact email"}), 400
    if not is_valid_phone(data['contact_phone']):
        return jsonify({"message": "Invalid contact phone"}), 400

    try:
        landlord = UserService.create_landlord_profile(user_id, data)
        return jsonify({"message": "Landlord profile created successfully", "landlord": landlord}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to create landlord profile"}), 500

@users_bp.put("/landlord-profile")
@jwt_required()
def update_landlord_profile():
    """Update landlord profile"""
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        landlord = UserService.update_landlord_profile(user_id, data)
        return jsonify({"message": "Landlord profile updated successfully", "landlord": landlord}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to update landlord profile"}), 500

@users_bp.get("/stats")
@jwt_required()
def get_user_stats():
    """Get user statistics"""
    user_id = get_jwt_identity()

    try:
        stats = UserService.get_user_stats(user_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": "Failed to get user stats"}), 500

@users_bp.delete("/account")
@jwt_required()
def deactivate_account():
    """Deactivate user account"""
    user_id = get_jwt_identity()

    try:
        UserService.deactivate_account(user_id)
        return jsonify({"message": "Account deactivated successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to deactivate account"}), 500

@users_bp.post("/verify-email")
@jwt_required()
def verify_email():
    """Verify user email"""
    user_id = get_jwt_identity()

    try:
        user = UserService.verify_email(user_id)
        return jsonify({"message": "Email verified successfully", "user": user}), 200
    except Exception as e:
        return jsonify({"message": "Failed to verify email"}), 500
