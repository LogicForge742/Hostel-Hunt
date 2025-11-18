from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def admin_required(fn):
    """
    Decorator to restrict access to admin users only.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            return {"message": "Admin access required"}, 403
        return fn(*args, **kwargs)
    return wrapper

def landlord_required(fn):
    """
    Decorator to restrict access to landlord users only.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "landlord":
            return {"message": "Landlord access required"}, 403
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    """
    Decorator to restrict access to student users only.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "student":
            return {"message": "Student access required"}, 403
        return fn(*args, **kwargs)
    return wrapper

