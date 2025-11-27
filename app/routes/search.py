from flask import Blueprint, request, jsonify
from ..services.search_service import SearchService

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.get("/hostels")
def search_hostels():
    """Advanced search for hostels"""
    try:
        query_params = request.args.to_dict(flat=False)

        # Convert single values to strings, keep lists as lists
        processed_params = {}
        for key, value in query_params.items():
            if len(value) == 1:
                processed_params[key] = value[0]
            else:
                processed_params[key] = value

        page = int(processed_params.pop('page', '1'))
        per_page = int(processed_params.pop('per_page', '20'))

        result = SearchService.search_hostels(processed_params, page=page, per_page=per_page)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Search failed", "error": str(e)}), 500

@search_bp.get("/suggestions")
def get_search_suggestions():
    """Get search suggestions"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))

        suggestions = SearchService.get_search_suggestions(query, limit)
        return jsonify({"suggestions": suggestions}), 200

    except Exception as e:
        return jsonify({"message": "Failed to get suggestions", "error": str(e)}), 500

@search_bp.get("/popular-locations")
def get_popular_locations():
    """Get popular locations"""
    try:
        limit = int(request.args.get('limit', 20))

        locations = SearchService.get_popular_locations(limit)
        return jsonify({"locations": locations}), 200

    except Exception as e:
        return jsonify({"message": "Failed to get popular locations", "error": str(e)}), 500

@search_bp.get("/price-ranges")
def get_price_ranges():
    """Get price range statistics"""
    try:
        ranges = SearchService.get_price_ranges()
        return jsonify(ranges), 200

    except Exception as e:
        return jsonify({"message": "Failed to get price ranges", "error": str(e)}), 500

@search_bp.get("/filters")
def get_filter_options():
    """Get available filter options"""
    try:
        options = SearchService.get_filter_options()
        return jsonify(options), 200

    except Exception as e:
        return jsonify({"message": "Failed to get filter options", "error": str(e)}), 500
