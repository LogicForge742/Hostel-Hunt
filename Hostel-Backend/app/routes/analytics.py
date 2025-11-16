from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.booking_service import BookingService
from ..services.hostel_service import HostelService
from ..middleware.auth_middleware import landlord_required
from datetime import datetime, timedelta

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.get("/landlord")
@jwt_required()
@landlord_required
def get_landlord_analytics():
    """Get comprehensive analytics for landlord dashboard"""
    user_id = get_jwt_identity()

    try:
        # Get landlord's hostels
        hostels_result = HostelService.get_hostels_by_landlord(user_id, page=1, per_page=1000)
        hostels = hostels_result.get('hostels', [])

        if not hostels:
            return jsonify({
                'totalRevenue': 0,
                'monthlyRevenue': 0,
                'totalBookings': 0,
                'activeBookings': 0,
                'occupancyRate': 0,
                'averageRating': 0,
                'topHostel': None,
                'monthlyTrend': [],
                'totalHostels': 0
            }), 200

        # Calculate analytics
        total_revenue = 0
        total_bookings = 0
        active_bookings = 0
        monthly_revenue = 0

        # Current month
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = current_month + timedelta(days=32)
        next_month = next_month.replace(day=1)

        # Monthly trend data (last 4 months)
        monthly_trend = []
        for i in range(3, -1, -1):
            month_start = current_month - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)

            month_revenue = 0
            month_bookings = 0

            # This would need to be implemented in the service
            # For now, return mock data structure
            monthly_trend.append({
                'month': month_start.strftime('%b'),
                'revenue': month_revenue,
                'bookings': month_bookings
            })

        # Get booking stats for all landlord's hostels
        booking_stats = BookingService.get_booking_stats(landlord_id=user_id)

        # Calculate occupancy rate (simplified)
        total_capacity = sum(hostel.get('capacity', 1) for hostel in hostels)
        occupancy_rate = min(100, (active_bookings / max(total_capacity, 1)) * 100) if total_capacity > 0 else 0

        # Find top performing hostel
        top_hostel = None
        if hostels:
            # This would need more complex logic to determine top hostel
            top_hostel = {
                'name': hostels[0]['name'],
                'revenue': booking_stats['total_revenue'],
                'bookings': booking_stats['confirmed_bookings'] + booking_stats['completed_bookings']
            }

        # Mock additional metrics
        average_rating = 4.2  # This would come from reviews

        return jsonify({
            'totalRevenue': booking_stats['total_revenue'],
            'monthlyRevenue': monthly_revenue,
            'totalBookings': booking_stats['total_bookings'],
            'activeBookings': active_bookings,
            'occupancyRate': round(occupancy_rate, 1),
            'averageRating': average_rating,
            'topHostel': top_hostel,
            'monthlyTrend': monthly_trend,
            'totalHostels': len(hostels)
        }), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch analytics", "error": str(e)}), 500
