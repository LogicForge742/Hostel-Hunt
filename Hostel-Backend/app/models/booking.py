from ..extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostels.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="KES")
    status = db.Column(db.String(20), default="confirmed")  # confirmed, cancelled, completed, upcoming
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='bookings')
    hostel = db.relationship('Hostel', back_populates='bookings')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hostel_id": self.hostel_id,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "guests": self.guests,
            "total_price": self.total_price,
            "currency": self.currency,
            "status": self.status,
            "booking_date": self.booking_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user": self.user.to_dict() if self.user else None,
            "hostel": self.hostel.to_dict() if self.hostel else None
        }
