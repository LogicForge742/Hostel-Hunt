from ..extensions import db
from datetime import datetime

class Hostel(db.Model):
    __tablename__ = "hostels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="KES")
    capacity = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)
    images = db.Column(db.JSON)
    amenities = db.Column(db.JSON)
    features = db.Column(db.JSON)
    availability = db.Column(db.JSON)
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    landlord = db.relationship('Landlord', back_populates='hostels')
    bookings = db.relationship('Booking', back_populates='hostel', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='hostel', cascade='all, delete-orphan')

    @property
    def available_rooms(self):
        """Calculate available rooms based on capacity minus current confirmed bookings"""
        from ..models.booking import Booking
        from datetime import date

        current_bookings = Booking.query.filter(
            Booking.hostel_id == self.id,
            Booking.status.in_(['confirmed', 'upcoming']),
            Booking.check_out >= date.today()
        ).all()

        occupied_guests = sum(booking.guests for booking in current_bookings)
        return max(0, self.capacity - occupied_guests)

    def to_dict(self):
        # Retrieve stored availability settings
        avail_settings = self.availability or {}
        
        # AUTO-UPDATE: If capacity is 0, force availability to False
        is_available = avail_settings.get('available', True)
        if self.available_rooms <= 0:
            is_available = False

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "price": self.price,
            "currency": self.currency,
            "capacity": self.capacity,
            "available_rooms": self.available_rooms,
            "room_type": self.room_type,
            "landlord_id": self.landlord_id,
            "images": self.images or [],
            "amenities": self.amenities or [],
            "features": self.features or {},
            # Merged availability logic
            "availability": {
                **avail_settings,
                "available": is_available 
            },
            "is_verified": self.is_verified,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "landlord": self.landlord.to_dict() if self.landlord else None
        }