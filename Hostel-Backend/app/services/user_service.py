from ..extensions import db
from ..models.user import User
from ..models.landlord import Landlord
from werkzeug.security import generate_password_hash
from datetime import datetime

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get_or_404(user_id)
        return user.to_dict()

    @staticmethod
    def update_user_profile(user_id, update_data):
        """Update user profile"""
        user = User.query.get_or_404(user_id)

        allowed_fields = ['name', 'phone_number', 'profile_image']
        try:
            for field in allowed_fields:
                if field in update_data:
                    setattr(user, field, update_data[field])

            user.updated_at = datetime.utcnow()
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def change_password(user_id, current_password, new_password):
        """Change user password"""
        user = User.query.get_or_404(user_id)

        if not user.check_password(current_password):
            raise ValueError("Current password is incorrect")

        try:
            user.set_password(new_password)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_landlord_profile(user_id, landlord_data):
        """Create landlord profile for a user"""
        user = User.query.get_or_404(user_id)

        # Check if user already has a landlord profile
        if user.landlord_profile:
            raise ValueError("User already has a landlord profile")

        try:
            # Update user role
            user.role = 'landlord'
            user.updated_at = datetime.utcnow()

            # Create landlord profile
            # Use the relationship to link the landlord to the user.
            landlord = Landlord(**landlord_data)
            landlord.user = user

            db.session.add(landlord)
            db.session.commit()
            return landlord.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_landlord_profile(user_id, update_data):
        """Update landlord profile"""
        user = User.query.get_or_404(user_id)

        if not user.landlord_profile:
            raise ValueError("User does not have a landlord profile")

        allowed_fields = [
            'business_name', 'contact_phone', 'contact_email',
            'address', 'description'
        ]

        try:
            for field in allowed_fields:
                if field in update_data:
                    setattr(user.landlord_profile, field, update_data[field])

            user.landlord_profile.updated_at = datetime.utcnow()
            db.session.commit()
            return user.landlord_profile.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_stats(user_id):
        """Get user statistics"""
        user = User.query.get_or_404(user_id)

        from ..models.booking import Booking
        from ..models.review import Review

        total_bookings = Booking.query.filter_by(user_id=user_id).count()
        active_bookings = Booking.query.filter_by(
            user_id=user_id,
            status='confirmed'
        ).count()
        total_reviews = Review.query.filter_by(user_id=user_id).count()

        # Calculate total spent
        total_spent = db.session.query(db.func.sum(Booking.total_price))\
            .filter(
                Booking.user_id == user_id,
                Booking.status.in_(['confirmed', 'completed'])
            ).scalar() or 0

        return {
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'total_reviews': total_reviews,
            'total_spent': float(total_spent)
        }

    @staticmethod
    def deactivate_account(user_id):
        """Deactivate user account"""
        user = User.query.get_or_404(user_id)

        try:
            user.is_active = False
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def verify_email(user_id):
        """Mark user email as verified"""
        user = User.query.get_or_404(user_id)

        try:
            user.email_verified = True
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_users_list(page=1, per_page=20, filters=None):
        """Get list of users (admin only)"""
        query = User.query

        if filters:
            if filters.get('role'):
                query = query.filter_by(role=filters['role'])
            if filters.get('is_active') is not None:
                query = query.filter_by(is_active=filters['is_active'])
            if filters.get('email_verified') is not None:
                query = query.filter_by(email_verified=filters['email_verified'])

        query = query.order_by(User.created_at.desc())

        users = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page
        }

    @staticmethod
    def update_user_role(user_id, new_role, admin_id):
        """Update user role (admin only)"""
        # Verify admin
        admin = User.query.get_or_404(admin_id)
        if admin.role != 'admin':
            raise ValueError("Unauthorized")

        user = User.query.get_or_404(user_id)

        valid_roles = ['student', 'landlord', 'admin']
        if new_role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")

        try:
            user.role = new_role
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
