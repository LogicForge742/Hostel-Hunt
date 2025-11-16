from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.review_service import ReviewService

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

@reviews_bp.post("/")
@jwt_required()
def create_review():
    """Create a new review"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    required_fields = ['hostel_id', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    rating = data['rating']
    if not (1 <= rating <= 5):
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    try:
        review = ReviewService.create_review(
            user_id=user_id,
            hostel_id=data['hostel_id'],
            rating=rating,
            comment=data.get('comment')
        )
        return jsonify({"message": "Review created successfully", "review": review}), 201

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to create review", "error": str(e)}), 500

@reviews_bp.put("/<int:review_id>")
@jwt_required()
def update_review(review_id):
    """Update an existing review"""
    user_id = get_jwt_identity()
    data = request.get_json()

    rating = data.get('rating')
    comment = data.get('comment')

    if rating is not None and not (1 <= rating <= 5):
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    try:
        review = ReviewService.update_review(
            review_id=review_id,
            user_id=user_id,
            rating=rating,
            comment=comment
        )
        return jsonify({"message": "Review updated successfully", "review": review}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to update review", "error": str(e)}), 500

@reviews_bp.delete("/<int:review_id>")
@jwt_required()
def delete_review(review_id):
    """Delete a review"""
    user_id = get_jwt_identity()

    try:
        ReviewService.delete_review(review_id, user_id)
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete review", "error": str(e)}), 500

@reviews_bp.get("/hostel/<int:hostel_id>")
def get_hostel_reviews(hostel_id):
    """Get all reviews for a hostel"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = ReviewService.get_hostel_reviews(
            hostel_id=hostel_id,
            page=page,
            per_page=per_page
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch reviews", "error": str(e)}), 500

@reviews_bp.get("/user")
@jwt_required()
def get_user_reviews():
    """Get all reviews by current user"""
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = ReviewService.get_user_reviews(
            user_id=user_id,
            page=page,
            per_page=per_page
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch user reviews", "error": str(e)}), 500

@reviews_bp.get("/<int:review_id>")
def get_review(review_id):
    """Get a specific review"""
    try:
        review = ReviewService.get_review_by_id(review_id)
        return jsonify(review), 200
    except Exception as e:
        return jsonify({"message": "Review not found"}), 404

@reviews_bp.get("/stats/<int:hostel_id>")
def get_review_stats(hostel_id):
    """Get review statistics for a hostel"""
    try:
        stats = ReviewService.get_reviews_stats(hostel_id=hostel_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": "Failed to get review stats", "error": str(e)}), 500
