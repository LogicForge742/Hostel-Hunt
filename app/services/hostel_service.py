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
            # Location Filter: Now searches Name, Location, AND University field
            if filters.get('location'):
                location_term = f"%{filters['location']}%"
                query = query.filter(
                    or_(
                        Hostel.location.ilike(location_term),
                        Hostel.name.ilike(location_term),
                        # NEW: Search inside the JSON features for the university name
                        func.cast(Hostel.features['university'], db.String).ilike(location_term)
                    )
                )

            if filters.get('min_price'):
                query = query.filter(Hostel.price >= filters['min_price'])
            if filters.get('max_price'):
                query = query.filter(Hostel.price <= filters['max_price'])

            if filters.get('room_type'):
                room_types = filters['room_type'] if isinstance(filters['room_type'], list) else [filters['room_type']]
                query = query.filter(Hostel.room_type.in_(room_types))

            if filters.get('min_capacity'):
                query = query.filter(Hostel.capacity >= filters['min_capacity'])

            if filters.get('verified_only'):
                query = query.filter(Hostel.is_verified == True)

        # Sorting
        sort_by = filters.get('sort_by', 'created_at') if filters else 'created_at'
        if sort_by == 'price_asc':
            query = query.order_by(Hostel.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Hostel.price.desc())
        else:
            query = query.order_by(Hostel.created_at.desc())

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

        avg_rating = db.session.query(func.avg(Review.rating)).filter(
            Review.hostel_id == hostel_id
        ).scalar() or 0.0

        review_count = Review.query.filter_by(hostel_id=hostel_id).count()
        features = hostel.features or {}
        availability = hostel.availability or {}

        location_parts = hostel.location.split(',') if hostel.location else ['', '']
        area = location_parts[0].strip() if len(location_parts) > 0 else ''
        city = location_parts[1].strip() if len(location_parts) > 1 else ''

        amenities_list = []
        if hostel.amenities and isinstance(hostel.amenities, list) and len(hostel.amenities) > 0:
            found_amenities = Amenity.query.filter(Amenity.id.in_(hostel.amenities)).all()
            amenities_list = [a.name for a in found_amenities]

        landlord_data = None
        if hostel.landlord:
            landlord_data = {
                'name': hostel.landlord.business_name or (hostel.landlord.user.name if hostel.landlord.user else 'Unknown'),
                'verified': hostel.landlord.is_verified,
                'rating': float(avg_rating),
                'reviewCount': review_count,
                'phone': hostel.landlord.contact_phone or (hostel.landlord.user.phone_number if hostel.landlord.user else 'Not Available')
            }

        availability_data = {
            'available': availability.get('available', True),
            'availableFrom': availability.get('available_from', '2024-01-01'),
            'minimumStay': availability.get('minimum_stay', '1 month'),
            'deposit': availability.get('deposit', 0)
        }

        price_includes = features.get('rent_included', [])
        # FIX: Corrected typo below (was notQP)
        if not price_includes: 
            price_includes = availability.get('price_includes', ['Water', 'Electricity'])

        formatted_room_type = hostel.room_type.replace('_', ' ').title()

        return {
            'id': hostel.id,
            'title': hostel.name,
            'description': hostel.description or '',
            'location': {
                'area': area,
                'city': city,
                'distance': '2.5 km from campus',
                'description': f'Located in {area}, {city}'
            },
            'price': hostel.price,
            'currency': hostel.currency,
            'capacity': hostel.capacity,
            'available_rooms': hostel.available_rooms,
            'roomType': formatted_room_type,
            'images': hostel.images or [],
            'amenities': amenities_list,
            'features': features,
            'availability': availability_data,
            'priceIncludes': price_includes,
            'featured': hostel.is_featured,
            'verified': hostel.is_verified,
            'landlord': landlord_data,
            'similarRooms': []
        }

    @staticmethod
    def create_hostel(hostel_data, landlord_id):
        from ..models.landlord import Landlord
        landlord = Landlord.query.filter_by(user_id=landlord_id).first()
        if not landlord:
            raise ValueError("Landlord profile not found")

        hostel = Hostel(
            landlord_id=landlord.id,
            **hostel_data
        )
        db.session.add(hostel)
        db.session.commit()
        return hostel.to_dict()

    @staticmethod
    def update_hostel(hostel_id, update_data, landlord_id):
        from ..models.landlord import Landlord
        landlord = Landlord.query.filter_by(user_id=landlord_id).first()
        if not landlord:
             raise ValueError("Landlord profile not found")

        hostel = Hostel.query.filter_by(
            id=hostel_id,
            landlord_id=landlord.id
        ).first_or_404()

        for key, value in update_data.items():
            if hasattr(hostel, key):
                setattr(hostel, key, value)

        hostel.updated_at = datetime.utcnow()
        db.session.commit()
        return hostel.to_dict()

    @staticmethod
    def delete_hostel(hostel_id, landlord_id):
        from ..models.landlord import Landlord
        landlord = Landlord.query.filter_by(user_id=landlord_id).first()
        if not landlord:
             raise ValueError("Landlord profile not found")

        hostel = Hostel.query.filter_by(
            id=hostel_id,
            landlord_id=landlord.id
        ).first_or_404()

        db.session.delete(hostel)
        db.session.commit()
        return True

    @staticmethod
    def get_hostels_by_landlord(landlord_id, page=1, per_page=20):
        from ..models.landlord import Landlord
        landlord = Landlord.query.filter_by(user_id=landlord_id).first()
        if not landlord:
            return {'hostels': [], 'total': 0, 'pages': 0, 'current_page': page}

        hostels = Hostel.query.filter_by(landlord_id=landlord.id)\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'hostels': [hostel.to_dict() for hostel in hostels.items],
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page
        }

    @staticmethod
    def search_hostels(query, page=1, per_page=20):
        search_term = f"%{query}%"
        # Also updated basic search to include university features
        hostels = Hostel.query.filter(
            or_(
                Hostel.name.ilike(search_term),
                Hostel.location.ilike(search_term),
                Hostel.description.ilike(search_term),
                func.cast(Hostel.features['university'], db.String).ilike(search_term)
            )
        ).paginate(page=page, per_page=per_page, error_out=False)

        return {
            'hostels': [hostel.to_dict() for hostel in hostels.items],
            'total': hostels.total,
            'pages': hostels.pages,
            'current_page': hostels.page
        }