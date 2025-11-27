from ..extensions import db
from ..models.booking import Booking
from ..models.hostel import Hostel
from datetime import datetime, date
from sqlalchemy import and_, or_

class BookingService:
    @staticmethod
    def create_booking(user_id, hostel_id, check_in, check_out, guests):
        """Create a new booking"""
        # Validate dates
        check_in_date = date.fromisoformat(check_in)
        check_out_date = date.fromisoformat(check_out)

        if check_in_date >= check_out_date:
            raise ValueError("Check-out date must be after check-in date")

        if check_in_date < date.today():
            raise ValueError("Check-in date cannot be in the past")

        # Check availability
        if not BookingService.check_availability(hostel_id, check_in_date, check_out_date, guests):
            raise ValueError("Hostel is not available for the selected dates")

        # Get hostel for pricing
        hostel = Hostel.query.get_or_404(hostel_id)

        # Calculate total price (per month per person)
        days = (check_out_date - check_in_date).days
        months = max(1, round(days / 30))  # At least 1 month, round to nearest month
        total_price = hostel.price * months * guests

        try:
            booking = Booking(
                user_id=user_id,
                hostel_id=hostel_id,
                check_in=check_in_date,
                check_out=check_out_date,
                guests=guests,
                total_price=total_price,
                status='confirmed'
            )

            db.session.add(booking)
            db.session.commit()
            return booking.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def check_availability(hostel_id, check_in, check_out, guests=1):
        """Check if a hostel is available for the given dates and number of guests"""
        # Get hostel capacity
        hostel = Hostel.query.get_or_404(hostel_id)
        max_capacity = hostel.capacity

        # Check for overlapping bookings and sum their guests
        overlapping_bookings = Booking.query.filter(
            and_(
                Booking.hostel_id == hostel_id,
                Booking.status.in_(['confirmed', 'upcoming']),
                or_(
                    and_(Booking.check_in <= check_in, Booking.check_out > check_in),
                    and_(Booking.check_in < check_out, Booking.check_out >= check_out),
                    and_(Booking.check_in >= check_in, Booking.check_out <= check_out)
                )
            )
        ).all()

        # Sum guests from overlapping bookings
        total_guests_booked = sum(booking.guests for booking in overlapping_bookings)

        # Check if adding new guests would exceed capacity
        return (total_guests_booked + guests) <= max_capacity

    @staticmethod
    def get_user_bookings(user_id, page=1, per_page=20, status=None):
        """Get all bookings for a user"""
        query = Booking.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        query = query.order_by(Booking.created_at.desc())

        bookings = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'bookings': [booking.to_dict() for booking in bookings.items],
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': bookings.page
        }

    @staticmethod
    def get_booking_by_id(booking_id, user_id=None):
        """Get a specific booking"""
        query = Booking.query.filter_by(id=booking_id)

        if user_id:
            query = query.filter_by(user_id=user_id)

        booking = query.first_or_404()
        return booking.to_dict()

    @staticmethod
    def cancel_booking(booking_id, user_id):
        """Cancel a booking"""
        booking = Booking.query.filter_by(
            id=booking_id,
            user_id=user_id
        ).first_or_404()

        if booking.status not in ['confirmed', 'upcoming']:
            raise ValueError("Cannot cancel this booking")

        if booking.check_in <= date.today():
            raise ValueError("Cannot cancel booking on or after check-in date")

        try:
            booking.status = 'cancelled'
            booking.updated_at = datetime.utcnow()
            db.session.commit()

            # Recalculate availability for the hostel (this will update the available_rooms property)
            # The available_rooms property in Hostel model automatically recalculates based on current bookings
            return booking.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_hostel_bookings(hostel_id, landlord_id, page=1, per_page=20):
        """Get all bookings for a hostel (landlord only)"""
        # Verify landlord owns the hostel
        hostel = Hostel.query.filter_by(
            id=hostel_id,
            landlord_id=landlord_id
        ).first_or_404()

        bookings = Booking.query.filter_by(hostel_id=hostel_id)\
            .order_by(Booking.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'bookings': [booking.to_dict() for booking in bookings.items],
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': bookings.page
        }

    @staticmethod
    def update_booking_status(booking_id, status, landlord_id=None):
        """Update booking status (for admin/landlord)"""
        booking = Booking.query.get_or_404(booking_id)

        # If landlord_id provided, verify they own the hostel
        if landlord_id:
            hostel = Hostel.query.filter_by(
                id=booking.hostel_id,
                landlord_id=landlord_id
            ).first_or_404()

        valid_statuses = ['confirmed', 'cancelled', 'completed', 'no_show']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        try:
            booking.status = status
            booking.updated_at = datetime.utcnow()
            db.session.commit()
            return booking.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_landlord_bookings(user_id, page=1, per_page=20, status=None):
        """Get all bookings for all hostels owned by a landlord"""
        # Get landlord profile to find landlord_id
        from ..models.user import User
        user = User.query.get_or_404(user_id)
        if not user.landlord_profile:
            raise ValueError("User is not a landlord")

        landlord_id = user.landlord_profile.id

        # Get all hostel IDs owned by the landlord
        hostels = Hostel.query.filter_by(landlord_id=landlord_id).all()
        hostel_ids = [h.id for h in hostels]

        if not hostel_ids:
            return {
                'bookings': [],
                'total': 0,
                'pages': 0,
                'current_page': page
            }

        query = Booking.query.filter(Booking.hostel_id.in_(hostel_ids))

        if status:
            query = query.filter_by(status=status)

        query = query.order_by(Booking.created_at.desc())

        bookings = query.paginate(page=page, per_page=per_page, error_out=False)

        # Enhance booking data with hostel and user info
        enhanced_bookings = []
        for booking in bookings.items:
            booking_dict = booking.to_dict()
            # Add hostel name and user info
            booking_dict['hostel_name'] = booking.hostel.name if booking.hostel else 'Unknown'
            booking_dict['customer_name'] = booking.user.name if booking.user else 'Unknown'
            booking_dict['customer_email'] = booking.user.email if booking.user else 'Unknown'
            enhanced_bookings.append(booking_dict)

        return {
            'bookings': enhanced_bookings,
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': bookings.page
        }

    @staticmethod
    def get_booking_stats(hostel_id=None, landlord_id=None):
        """Get booking statistics"""
        query = Booking.query

        if hostel_id:
            query = query.filter_by(hostel_id=hostel_id)
        elif landlord_id:
            # Get all bookings for landlord's hostels
            hostels = Hostel.query.filter_by(landlord_id=landlord_id).all()
            hostel_ids = [h.id for h in hostels]
            query = query.filter(Booking.hostel_id.in_(hostel_ids))

        total_bookings = query.count()
        confirmed_bookings = query.filter_by(status='confirmed').count()
        cancelled_bookings = query.filter_by(status='cancelled').count()
        completed_bookings = query.filter_by(status='completed').count()

        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Booking.total_price))\
            .filter(Booking.status.in_(['confirmed', 'completed']))\
            .scalar() or 0

        return {
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'completed_bookings': completed_bookings,
            'total_revenue': float(total_revenue)
        }
