from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_service import UserService
from ..services.hostel_service import HostelService
from ..services.booking_service import BookingService
from ..services.review_service import ReviewService
from ..middleware.auth_middleware import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.get("/users")
@jwt_required()
@admin_required
def get_users():
    """Get all users (admin only)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        filters = {
            'role': request.args.get('role'),
            'is_active': request.args.get('is_active'),
            'email_verified': request.args.get('email_verified')
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        result = UserService.get_users_list(page=page, per_page=per_page, filters=filters)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch users", "error": str(e)}), 500

@admin_bp.put("/users/<int:user_id>/role")
@jwt_required()
@admin_required
def update_user_role(user_id):
    """Update user role (admin only)"""
    admin_id = get_jwt_identity()
    data = request.get_json()

    new_role = data.get('role')
    if not new_role:
        return jsonify({"message": "Role is required"}), 400

    try:
        user = UserService.update_user_role(user_id, new_role, admin_id)
        return jsonify({"message": "User role updated successfully", "user": user}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to update user role", "error": str(e)}), 500

@admin_bp.put("/hostels/<int:hostel_id>/verify")
@jwt_required()
@admin_required
def verify_hostel(hostel_id):
    """Verify a hostel (admin only)"""
    data = request.get_json()
    is_verified = data.get('is_verified', True)

    try:
        # Get hostel
        hostel = HostelService.get_hostel_by_id(hostel_id)

        # Update verification status
        update_data = {'is_verified': is_verified}
        updated_hostel = HostelService.update_hostel(hostel_id, update_data, hostel['landlord_id'])

        return jsonify({"message": "Hostel verification updated successfully", "hostel": updated_hostel}), 200

    except Exception as e:
        return jsonify({"message": "Failed to update hostel verification", "error": str(e)}), 500

@admin_bp.put("/hostels/<int:hostel_id>/feature")
@jwt_required()
@admin_required
def feature_hostel(hostel_id):
    """Feature or unfeature a hostel (admin only)"""
    data = request.get_json()
    is_featured = data.get('is_featured', True)

    try:
        # Get hostel
        hostel = HostelService.get_hostel_by_id(hostel_id)

        # Update featured status
        update_data = {'is_featured': is_featured}
        updated_hostel = HostelService.update_hostel(hostel_id, update_data, hostel['landlord_id'])

        return jsonify({"message": "Hostel feature status updated successfully", "hostel": updated_hostel}), 200

    except Exception as e:
        return jsonify({"message": "Failed to update hostel feature status", "error": str(e)}), 500

@admin_bp.get("/stats")
@jwt_required()
@admin_required
def get_admin_stats():
    """Get admin statistics"""
    try:
        # User stats
        total_users = UserService.get_users_list(page=1, per_page=1)['total']
        active_users = UserService.get_users_list(page=1, per_page=1, filters={'is_active': True})['total']
        verified_users = UserService.get_users_list(page=1, per_page=1, filters={'email_verified': True})['total']

        # Hostel stats
        all_hostels = HostelService.get_all_hostels(page=1, per_page=1)
        total_hostels = all_hostels['total']
        verified_hostels = HostelService.get_all_hostels(page=1, per_page=1, filters={'verified_only': True})['total']
        featured_hostels = HostelService.get_all_hostels(page=1, per_page=1, filters={'featured_only': True})['total']

        # Booking stats
        booking_stats = BookingService.get_booking_stats()

        # Review stats
        review_stats = ReviewService.get_reviews_stats()

        stats = {
            'users': {
                'total': total_users,
                'active': active_users,
                'verified': verified_users
            },
            'hostels': {
                'total': total_hostels,
                'verified': verified_hostels,
                'featured': featured_hostels
            },
            'bookings': booking_stats,
            'reviews': review_stats
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"message": "Failed to get admin stats", "error": str(e)}), 500

@admin_bp.delete("/reviews/<int:review_id>")
@jwt_required()
@admin_required
def delete_review_admin(review_id):
    """Delete any review (admin only)"""
    try:
        # Get review to find user_id
        review = ReviewService.get_review_by_id(review_id)
        ReviewService.delete_review(review_id, review['user_id'])
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete review", "error": str(e)}), 500

@admin_bp.put("/bookings/<int:booking_id>/status")
@jwt_required()
@admin_required
def update_booking_status_admin(booking_id):
    """Update any booking status (admin only)"""
    data = request.get_json()
    status = data.get('status')

    if not status:
        return jsonify({"message": "Status is required"}), 400

    try:
        booking = BookingService.update_booking_status(booking_id, status)
        return jsonify({"message": "Booking status updated successfully", "booking": booking}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to update booking status", "error": str(e)}), 500
