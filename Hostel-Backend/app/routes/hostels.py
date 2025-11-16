from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.hostel_service import HostelService
from ..middleware.auth_middleware import landlord_required
from ..utils.validator import is_valid_email

hostels_bp = Blueprint("hostels", __name__, url_prefix="/hostels/")

@hostels_bp.get("/")
def get_hostels():
    """Get all hostels with filtering and pagination"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        filters = {
            'location': request.args.get('location'),
            'min_price': request.args.get('min_price'),
            'max_price': request.args.get('max_price'),
            'room_type': request.args.getlist('room_type'),
            'min_capacity': request.args.get('min_capacity'),
            'amenities': request.args.getlist('amenities'),
            'furnished': request.args.get('furnished'),
            'verified_only': request.args.get('verified_only'),
            'featured_only': request.args.get('featured_only'),
            'sort_by': request.args.get('sort_by')
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        result = HostelService.get_all_hostels(page=page, per_page=per_page, filters=filters)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch hostels", "error": str(e)}), 500

@hostels_bp.get("/<int:hostel_id>")
def get_hostel(hostel_id):
    """Get a specific hostel by ID"""
    try:
        hostel = HostelService.get_hostel_by_id(hostel_id)
        return jsonify(hostel), 200
    except Exception as e:
        return jsonify({"message": "Hostel not found"}), 404

@hostels_bp.post("/")
@jwt_required()
@landlord_required
def create_hostel():
    """Create a new hostel (landlords only)"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'location', 'price', 'capacity', 'room_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    # Validate data types
    try:
        data['price'] = float(data['price'])
        data['capacity'] = int(data['capacity'])
        if 'latitude' in data:
            data['latitude'] = float(data['latitude'])
        if 'longitude' in data:
            data['longitude'] = float(data['longitude'])
    except ValueError:
        return jsonify({"message": "Invalid data types"}), 400

    try:
        hostel = HostelService.create_hostel(data, user_id)
        return jsonify({"message": "Hostel created successfully", "hostel": hostel}), 201
    except Exception as e:
        return jsonify({"message": "Failed to create hostel", "error": str(e)}), 500

@hostels_bp.put("/<int:hostel_id>")
@jwt_required()
@landlord_required
def update_hostel(hostel_id):
    """Update a hostel (landlord only)"""
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        hostel = HostelService.update_hostel(hostel_id, data, user_id)
        return jsonify({"message": "Hostel updated successfully", "hostel": hostel}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update hostel", "error": str(e)}), 500

@hostels_bp.delete("/<int:hostel_id>")
@jwt_required()
@landlord_required
def delete_hostel(hostel_id):
    """Delete a hostel (landlord only)"""
    user_id = get_jwt_identity()

    try:
        HostelService.delete_hostel(hostel_id, user_id)
        return jsonify({"message": "Hostel deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete hostel", "error": str(e)}), 500

@hostels_bp.get("/my-hostels")
@jwt_required()
@landlord_required
def get_my_hostels():
    """Get hostels owned by current landlord"""
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = HostelService.get_hostels_by_landlord(user_id, page=page, per_page=per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch hostels", "error": str(e)}), 500

@hostels_bp.get("/search")
def search_hostels():
    """Search hostels by query"""
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        if not query:
            return jsonify({"message": "Search query is required"}), 400

        result = HostelService.search_hostels(query, page=page, per_page=per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Search failed", "error": str(e)}), 500
