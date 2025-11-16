from ..extensions import db
from ..models.hostel import Hostel
from ..models.amenity import Amenity
from sqlalchemy import and_, or_, func, text
from sqlalchemy.sql import label
from geopy.distance import geodesic
import re

class SearchService:
    @staticmethod
    def search_hostels(query_params, page=1, per_page=20):
        """Advanced search for hostels with multiple filters"""
        query = Hostel.query

        # Text search (name, location, description)
        if query_params.get('q'):
            search_term = f"%{query_params['q']}%"
            query = query.filter(
                or_(
                    Hostel.name.ilike(search_term),
                    Hostel.location.ilike(search_term),
                    Hostel.description.ilike(search_term)
                )
            )

        # Location-based search
        if query_params.get('lat') and query_params.get('lng'):
            user_location = (float(query_params['lat']), float(query_params['lng']))
            radius = float(query_params.get('radius', 10))  # Default 10km radius

            # Filter hostels within radius (requires latitude/longitude columns)
            # This is a simplified version - in production, you'd use PostGIS or similar
            hostels_in_radius = []
            all_hostels = Hostel.query.filter(
                Hostel.latitude.isnot(None),
                Hostel.longitude.isnot(None)
            ).all()

            for hostel in all_hostels:
                hostel_location = (hostel.latitude, hostel.longitude)
                distance = geodesic(user_location, hostel_location).kilometers
                if distance <= radius:
                    hostels_in_radius.append(hostel.id)

            if hostels_in_radius:
                query = query.filter(Hostel.id.in_(hostels_in_radius))
            else:
                # No hostels in radius, return empty result
                query = query.filter(Hostel.id == -1)

        # Price range
        if query_params.get('min_price'):
            query = query.filter(Hostel.price >= float(query_params['min_price']))
        if query_params.get('max_price'):
            query = query.filter(Hostel.price <= float(query_params['max_price']))

        # Room type
        if query_params.get('room_type'):
            room_types = query_params['room_type'] if isinstance(query_params['room_type'], list) else [query_params['room_type']]
            query = query.filter(Hostel.room_type.in_(room_types))

        # Capacity
        if query_params.get('min_capacity'):
            query = query.filter(Hostel.capacity >= int(query_params['min_capacity']))

        # Amenities
        if query_params.get('amenities'):
            amenities = query_params['amenities'] if isinstance(query_params['amenities'], list) else [query_params['amenities']]
            # Filter hostels that have the selected amenities
            # amenities is expected to be a list of amenity keys like ['wifi', 'water', etc.]
            for amenity_key in amenities:
                # Check if the amenity exists in the hostel's amenities JSON
                query = query.filter(
                    Hostel.amenities[amenity_key].as_boolean() == True
                )

        # Features
        if query_params.get('furnished') is not None:
            furnished = query_params['furnished'].lower() in ('true', '1', 'yes')
            query = query.filter(
                Hostel.features['furnished'].as_boolean() == furnished
            )

        # Availability dates
        if query_params.get('check_in') and query_params.get('check_out'):
            from ..models.booking import Booking
            from datetime import datetime
            check_in = datetime.fromisoformat(query_params['check_in']).date()
            check_out = datetime.fromisoformat(query_params['check_out']).date()

            # Subquery to find hostels with conflicting bookings
            conflicting_bookings = db.session.query(Booking.hostel_id).filter(
                and_(
                    Booking.status.in_(['confirmed', 'upcoming']),
                    or_(
                        and_(Booking.check_in <= check_in, Booking.check_out > check_in),
                        and_(Booking.check_in < check_out, Booking.check_out >= check_out),
                        and_(Booking.check_in >= check_in, Booking.check_out <= check_out)
                    )
                )
            ).subquery()

            query = query.filter(~Hostel.id.in_(db.session.query(conflicting_bookings)))

        # Verification status
        if query_params.get('verified_only'):
            verified = query_params['verified_only'].lower() in ('true', '1', 'yes')
            query = query.filter(Hostel.is_verified == verified)

        # Featured hostels
        if query_params.get('featured_only'):
            featured = query_params['featured_only'].lower() in ('true', '1', 'yes')
            query = query.filter(Hostel.is_featured == featured)

        # Sorting
        sort_by = query_params.get('sort_by', 'relevance')
        if sort_by == 'price_asc':
            query = query.order_by(Hostel.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Hostel.price.desc())
        elif sort_by == 'rating':
            # Join with reviews to sort by average rating
            query = query.outerjoin(Hostel.reviews).group_by(Hostel.id)\
                .order_by(func.avg(Review.rating).desc().nulls_last())
        elif sort_by == 'newest':
            query = query.order_by(Hostel.created_at.desc())
        else:  # relevance or default
            query = query.order_by(Hostel.created_at.desc())

        # Pagination
        hostels = query.paginate(page=page, per_page=per_page, error_out=False)

        # Add average rating and review count to each hostel
        result_hostels = []
        for hostel in hostels.items:
            hostel_data = hostel.to_dict()

            # Calculate average rating
            avg_rating = db.session.query(func.avg(Review.rating))\
                .filter(Review.hostel_id == hostel.id)\
                .scalar() or 0.0

            review_count = Review.query.filter_by(hostel_id=hostel.id).count()

            hostel_data['average_rating'] = float(avg_rating)
            hostel_data['review_count'] = review_count

            result_hostels.append(hostel_data)

        return {
            'hostels': result_hostels,
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page,
            'per_page': hostels.per_page,
            'query': query_params.get('q', ''),
            'filters_applied': {k: v for k, v in query_params.items() if k != 'page' and k != 'per_page'}
        }

    @staticmethod
    def get_search_suggestions(query, limit=10):
        """Get search suggestions based on hostel names and locations"""
        if not query or len(query) < 2:
            return []

        search_term = f"{query}%"

        # Get matching hostel names
        names = db.session.query(
            label('text', Hostel.name),
            label('type', text("'hostel'"))
        ).filter(Hostel.name.ilike(search_term)).limit(limit//2)

        # Get matching locations
        locations = db.session.query(
            label('text', Hostel.location),
            label('type', text("'location'"))
        ).filter(Hostel.location.ilike(search_term)).limit(limit//2)

        # Combine and deduplicate
        suggestions = []
        seen = set()

        for result in names.union(locations).all():
            if result.text not in seen:
                suggestions.append({
                    'text': result.text,
                    'type': result.type
                })
                seen.add(result.text)

        return suggestions[:limit]

    @staticmethod
    def get_popular_locations(limit=20):
        """Get popular locations based on hostel count"""
        locations = db.session.query(
            Hostel.location,
            func.count(Hostel.id).label('hostel_count')
        ).group_by(Hostel.location)\
         .order_by(func.count(Hostel.id).desc())\
         .limit(limit)\
         .all()

        return [
            {
                'location': loc.location,
                'hostel_count': loc.hostel_count
            } for loc in locations
        ]

    @staticmethod
    def get_price_ranges():
        """Get price range statistics"""
        # Get basic stats
        price_stats = db.session.query(
            func.min(Hostel.price).label('min_price'),
            func.max(Hostel.price).label('max_price'),
            func.avg(Hostel.price).label('avg_price')
        ).first()

        # Get percentiles manually for SQLite compatibility
        all_prices = db.session.query(Hostel.price).filter(Hostel.price.isnot(None)).all()
        prices = sorted([p[0] for p in all_prices if p[0] is not None])

        if not prices:
            return {
                'min_price': 0,
                'max_price': 0,
                'avg_price': 0,
                'q1_price': 0,
                'q3_price': 0
            }

        n = len(prices)
        q1_index = int(0.25 * (n - 1))
        q3_index = int(0.75 * (n - 1))

        return {
            'min_price': float(price_stats.min_price or 0),
            'max_price': float(price_stats.max_price or 0),
            'avg_price': float(price_stats.avg_price or 0),
            'q1_price': float(prices[q1_index]),
            'q3_price': float(prices[q3_index])
        }

    @staticmethod
    def get_filter_options():
        """Get available filter options for search"""
        # Room types
        room_types = db.session.query(Hostel.room_type)\
            .distinct()\
            .filter(Hostel.room_type.isnot(None))\
            .all()

        # Amenities
        amenities = Amenity.query.all()

        return {
            'room_types': [rt[0] for rt in room_types],
            'amenities': [amenity.to_dict() for amenity in amenities],
            'price_ranges': SearchService.get_price_ranges(),
            'popular_locations': SearchService.get_popular_locations()
        }
