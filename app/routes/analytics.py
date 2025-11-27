from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..middleware.auth_middleware import landlord_required
from ..extensions import db
from ..models.hostel import Hostel
from ..models.booking import Booking
# FIX: Added 'text' to imports to fix the 500 error
from sqlalchemy import func, and_, text
from datetime import datetime, timedelta

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.get("/landlord")
@jwt_required()
@landlord_required
def get_landlord_analytics():
    """Get comprehensive analytics for landlord dashboard"""
    user_id = get_jwt_identity()

    try:
        # 1. Identify Landlord Profile
        from ..models.landlord import Landlord
        landlord = Landlord.query.filter_by(user_id=user_id).first()
        if not landlord:
            return jsonify({"message": "Landlord profile not found"}), 404

        # 2. Get all hostels owned by this landlord
        hostels = Hostel.query.filter_by(landlord_id=landlord.id).all()
        hostel_ids = [h.id for h in hostels]

        # Handle case with no hostels
        if not hostel_ids:
            return jsonify({
                'totalRevenue': 0, 'monthlyRevenue': 0, 'totalBookings': 0,
                'activeBookings': 0, 'occupancyRate': 0, 'averageRating': 0,
                'topHostel': None, 'monthlyTrend': [], 'totalHostels': 0
            }), 200

        # 3. Calculate Total Stats
        total_bookings = Booking.query.filter(Booking.hostel_id.in_(hostel_ids)).count()
        
        active_bookings = Booking.query.filter(
            Booking.hostel_id.in_(hostel_ids),
            Booking.status == 'confirmed',
            Booking.check_out >= datetime.utcnow().date()
        ).count()

        # Total Revenue (Sum of all confirmed/completed bookings)
        total_revenue = db.session.query(func.sum(Booking.total_price)).filter(
            Booking.hostel_id.in_(hostel_ids),
            Booking.status.in_(['confirmed', 'completed'])
        ).scalar() or 0

        # 4. Calculate Monthly Revenue (Current Month)
        today = datetime.utcnow()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_revenue = db.session.query(func.sum(Booking.total_price)).filter(
            Booking.hostel_id.in_(hostel_ids),
            Booking.status.in_(['confirmed', 'completed']),
            Booking.created_at >= start_of_month
        ).scalar() or 0

        # 5. Calculate Monthly Trend (Last 4 Months)
        monthly_trend = []
        for i in range(3, -1, -1):
            # Calculate start and end of the target month
            month_date = today - timedelta(days=30 * i)
            month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Logic to find next month start
            if month_start.month == 12:
                next_month_start = month_start.replace(year=month_start.year + 1, month=1)
            else:
                next_month_start = month_start.replace(month=month_start.month + 1)

            rev = db.session.query(func.sum(Booking.total_price)).filter(
                Booking.hostel_id.in_(hostel_ids),
                Booking.status.in_(['confirmed', 'completed']),
                Booking.created_at >= month_start,
                Booking.created_at < next_month_start
            ).scalar() or 0

            monthly_trend.append({
                'month': month_start.strftime('%b'),
                'revenue': float(rev),
                'bookings': Booking.query.filter(
                    Booking.hostel_id.in_(hostel_ids),
                    Booking.created_at >= month_start,
                    Booking.created_at < next_month_start
                ).count()
            })

        # 6. Calculate Occupancy Rate
        total_capacity = sum(h.capacity for h in hostels)
        occupancy_rate = 0
        if total_capacity > 0:
            occupancy_rate = round((active_bookings / total_capacity) * 100, 1)

        # 7. Identify Top Hostel (by Revenue)
        # NOTE: text() is now imported correctly
        top_hostel_query = db.session.query(
            Hostel.name, 
            func.sum(Booking.total_price).label('revenue'),
            func.count(Booking.id).label('count')
        ).join(Booking).filter(
            Hostel.landlord_id == landlord.id,
            Booking.status.in_(['confirmed', 'completed'])
        ).group_by(Hostel.name).order_by(text('revenue DESC')).first()

        top_hostel = None
        if top_hostel_query:
            top_hostel = {
                'name': top_hostel_query.name,
                'revenue': float(top_hostel_query.revenue),
                'bookings': top_hostel_query.count
            }
        elif hostels:
            # Fallback if no bookings yet
            top_hostel = {'name': hostels[0].name, 'revenue': 0, 'bookings': 0}

        return jsonify({
            'totalRevenue': float(total_revenue),
            'monthlyRevenue': float(monthly_revenue),
            'totalBookings': total_bookings,
            'activeBookings': active_bookings,
            'occupancyRate': occupancy_rate,
            'averageRating': round(landlord.rating, 1) if landlord.rating else 0,
            'topHostel': top_hostel,
            'monthlyTrend': monthly_trend,
            'totalHostels': len(hostels)
        }), 200

    except Exception as e:
        print(f"Analytics Error: {e}") # This prints to your terminal
        return jsonify({"message": "Failed to fetch analytics", "error": str(e)}), 500