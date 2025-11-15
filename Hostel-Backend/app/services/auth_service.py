from app.models.user import User
from app.extensions.db import db
from app.utils.jwt_utils import generate_tokens


class AuthService:
    @staticmethod
    def register(email, password, name=None, phone_number=None):
        """Register a new user.

        Accepts optional name and phone_number and stores them on the User.
        Returns (response_dict, None) on success, or (None, error_message) on failure.
        """
        if not email or not password:
            return None, "Email and password are required"

        existing = User.query.filter_by(email=email).first()
        if existing:
            return None, "Email already exists"

        user = User(email=email, name=name, phone_number=phone_number)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        tokens = generate_tokens(user.id)

        return {
            "user": user.to_dict(),
            "tokens": tokens
        }, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "Invalid email or password"

        tokens = generate_tokens(user.id)

        return {
            "user": user.to_dict(),
            "tokens": tokens
        }, None
