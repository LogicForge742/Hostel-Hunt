from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_service import UserService
from ..utils.validator import is_valid_email, is_valid_password, is_valid_phone

users_bp = Blueprint("users", __name__, url_prefix="/users")

# CORS Preflight Support
@users_bp.route("/profile", methods=["OPTIONS"])
def profile_options():
    return "", 200

@users_bp.route("/password", methods=["OPTIONS"])
def password_options():
    return "", 200

@users_bp.route("/become-landlord", methods=["OPTIONS"])
def become_landlord_options():
    return "", 200

@users_bp.route("/landlord-profile", methods=["OPTIONS"])
def landlord_profile_options():
    return "", 200


@users_bp.get("/profile")
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user), 200
    except Exception:
        return jsonify({"message": "User not found"}), 404

@users_bp.put("/profile")
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input data
    if 'email' in data:
        return jsonify({"message": "Email cannot be updated via this endpoint"}), 400
    if 'phone_number' in data and not is_valid_phone(data['phone_number']):
        return jsonify({"message": "Invalid phone number"}), 400

    try:
        user = UserService.update_user_profile(user_id, data)
        return jsonify({"message": "Profile updated successfully", "user": user}), 200
    except Exception as e:
        # Catch 404 from service if user is somehow deleted mid-request
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
    except Exception:
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
    except Exception:
        return jsonify({"message": "Failed to create landlord profile"}), 500

@users_bp.get("/landlord-profile")
@jwt_required()
def get_landlord_profile():
    """Get current user's landlord profile"""
    user_id = get_jwt_identity()
    try:
        # Re-using a pattern similar to get_user_by_id, but for the landlord profile.
        # This function will need to be added to UserService.
        landlord = UserService.get_landlord_profile_by_user_id(user_id)
        return jsonify(landlord), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception:
        return jsonify({"message": "Failed to fetch landlord profile"}), 500

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
    except Exception:
        return jsonify({"message": "Failed to update landlord profile"}), 500

@users_bp.get("/stats")
@jwt_required()
def get_user_stats():
    """Get user statistics"""
    user_id = get_jwt_identity()

    try:
        stats = UserService.get_user_stats(user_id)
        return jsonify(stats), 200
    except Exception:
        return jsonify({"message": "Failed to get user stats"}), 500

@users_bp.delete("/account")
@jwt_required()
def deactivate_account():
    """Deactivate user account"""
    user_id = get_jwt_identity()

    try:
        UserService.deactivate_account(user_id)
        # Note: In a real app, you might want to log the user out after this.
        return jsonify({"message": "Account deactivated successfully"}), 200
    except Exception:
        return jsonify({"message": "Failed to deactivate account"}), 500

@users_bp.post("/verify-email")
@jwt_required()
def verify_email():
    """Verify user email"""
    user_id = get_jwt_identity()

    try:
        user = UserService.verify_email(user_id)
        return jsonify({"message": "Email verified successfully", "user": user}), 200
    except Exception:
        return jsonify({"message": "Failed to verify email"}), 500

# --- Admin Endpoints ---

@users_bp.get("/list")
@jwt_required()
def get_users_list():
    """Get list of users (Admin only)"""
    admin_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    filters = {
        'role': request.args.get('role'),
        'is_active': request.args.get('is_active', type=lambda v: v.lower() == 'true' if v else None),
        'email_verified': request.args.get('email_verified', type=lambda v: v.lower() == 'true' if v else None)
    }
    
    # Filter out None values
    filters = {k: v for k, v in filters.items() if v is not None}

    try:
        # UserService.get_users_list handles the admin role check internally
        users_list = UserService.get_users_list(page=page, per_page=per_page, filters=filters, admin_id=admin_id)
        return jsonify(users_list), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 403 # Forbidden for non-admins
    except Exception:
        return jsonify({"message": "Failed to retrieve user list"}), 500

@users_bp.put("/<int:user_id>/role")
@jwt_required()
def update_user_role(user_id):
    """Update user role (Admin only)"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    new_role = data.get('role')

    if not new_role:
        return jsonify({"message": "Role field is required"}), 400

    try:
        user = UserService.update_user_role(user_id, new_role, admin_id)
        return jsonify({"message": f"User {user_id} role updated to {new_role}", "user": user}), 200
    except ValueError as e:
        # Handles "Unauthorized" (non-admin) and "Invalid role"
        status_code = 403 if "Unauthorized" in str(e) else 400
        return jsonify({"message": str(e)}), status_code
    except Exception:
        return jsonify({"message": f"Failed to update