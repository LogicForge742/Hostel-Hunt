from app.models.user import User
from app.models.landlord import Landlord
from ..extensions import db
from app.utils.jwt_utils import generate_tokens
from .email_service import EmailService


class AuthService:
    @staticmethod
    def register(email, password, name=None, phone_number=None, role="student"):
        """Register a new user.

        Accepts optional name, phone_number, and role and stores them on the User.
        Returns (response_dict, None) on success, or (None, error_message) on failure.
        """
        if not email or not password:
            return None, "Email and password are required"

        existing = User.query.filter_by(email=email).first()
        if existing:
            return None, "Email already exists"

        user = User(email=email, name=name, phone_number=phone_number, role=role)
        user.set_password(password)
        db.session.add(user)

        try:
            # Create landlord profile if role is landlord
            if role == "landlord":
                landlord = Landlord(user_id=user.id, contact_email=email, contact_phone=phone_number)
                db.session.add(landlord)

            # Commit user and landlord (if applicable) in one transaction
            db.session.commit()

            # Send a welcome email
            EmailService.send_welcome_email(user.email, user.name)

        except Exception as e:
            db.session.rollback()
            # Log the exception e in a real application
            return None, f"An error occurred during registration: {str(e)}"

        tokens = generate_tokens(user.id)


        return {
            "user": user.to_dict(),
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        }, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "Invalid email or password"

        if not user.is_active:
            return None, "Invalid email or password"

        tokens = generate_tokens(user.id)

        return {
            "user": user.to_dict(),
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        }, None
