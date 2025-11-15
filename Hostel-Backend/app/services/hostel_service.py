from ..extensions import db
from ..models.hostel import Hostel
from ..models.amenity import Amenity
from ..models.review import Review
from sqlalchemy import and_, or_, func
from datetime import datetime

class HostelService:
    @staticmethod
    def get_all_hostels(page=1, per_page=20, filters=None):
        """Get all hostels with pagination and filters"""
        query = Hostel.query

        if filters:
            # Location filter
            if filters.get('location'):
                location_term = f"%{filters['location']}%"
                query = query.filter(
                    or_(
                        Hostel.location.ilike(location_term),
                        Hostel.name.ilike(location_term)
                    )
                )

            # Price range filter
            if filters.get('min_price'):
                query = query.filter(Hostel.price >= filters['min_price'])
            if filters.get('max_price'):
                query = query.filter(Hostel.price <= filters['max_price'])

            # Room type filter
            if filters.get('room_type'):
                query = query.filter(Hostel.room_type.in_(filters['room_type']))

            # Capacity filter
            if filters.get('min_capacity'):
                query = query.filter(Hostel.capacity >= filters['min_capacity'])

            # Amenities filter
            if filters.get('amenities'):
                for amenity_id in filters['amenities']:
                    query = query.filter(
                        Hostel.amenities.cast(db.Text).contains(str(amenity_id))
                    )

            # Features filter
            if filters.get('furnished') is not None:
                query = query.filter(
                    Hostel.features['furnished'].as_boolean() == filters['furnished']
                )

            # Verification filter
            if filters.get('verified_only'):
                query = query.filter(Hostel.is_verified == True)

        # Sorting
        sort_by = filters.get('sort_by', 'created_at') if filters else 'created_at'
        if sort_by == 'price_asc':
            query = query.order_by(Hostel.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Hostel.price.desc())
        elif sort_by == 'rating':
            # This would require a subquery for average rating
            query = query.order_by(Hostel.created_at.desc())
        else:
            query = query.order_by(Hostel.created_at.desc())

        # Pagination
        hostels = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'hostels': [hostel.to_dict() for hostel in hostels.items],
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page,
            'per_page': hostels.per_page
        }

    @staticmethod
    def get_hostel_by_id(hostel_id):
        """Get a single hostel by ID with related data"""
        hostel = Hostel.query.get_or_404(hostel_id)

        # Calculate average rating
        avg_rating = db.session.query(func.avg(Review.rating)).filter(
            Review.hostel_id == hostel_id
        ).scalar() or 0.0

        # Get review count
        review_count = Review.query.filter_by(hostel_id=hostel_id).count()

        hostel_data = hostel.to_dict()
        hostel_data['average_rating'] = float(avg_rating)
        hostel_data['review_count'] = review_count

        return hostel_data

    @staticmethod
    def create_hostel(hostel_data, landlord_id):
        """Create a new hostel"""
        try:
            hostel = Hostel(
                landlord_id=landlord_id,
                **hostel_data
            )
            db.session.add(hostel)
            db.session.commit()
            return hostel.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_hostel(hostel_id, update_data, landlord_id):
        """Update an existing hostel"""
        hostel = Hostel.query.filter_by(
            id=hostel_id,
            landlord_id=landlord_id
        ).first_or_404()

        try:
            for key, value in update_data.items():
                if hasattr(hostel, key):
                    setattr(hostel, key, value)

            hostel.updated_at = datetime.utcnow()
            db.session.commit()
            return hostel.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_hostel(hostel_id, landlord_id):
        """Delete a hostel"""
        hostel = Hostel.query.filter_by(
            id=hostel_id,
            landlord_id=landlord_id
        ).first_or_404()

        try:
            db.session.delete(hostel)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_hostels_by_landlord(landlord_id, page=1, per_page=20):
        """Get all hostels for a specific landlord"""
        hostels = Hostel.query.filter_by(landlord_id=landlord_id)\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'hostels': [hostel.to_dict() for hostel in hostels.items],
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page
        }

    @staticmethod
    def search_hostels(query, page=1, per_page=20):
        """Search hostels by name, location, or description"""
        search_term = f"%{query}%"
        hostels = Hostel.query.filter(
            or_(
                Hostel.name.ilike(search_term),
                Hostel.location.ilike(search_term),
                Hostel.description.ilike(search_term)
            )
        ).paginate(page=page, per_page=per_page, error_out=False)

        return {
            'hostels': [hostel.to_dict() for hostel in hostels.items],
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page
        }
