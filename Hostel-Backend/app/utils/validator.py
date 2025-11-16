import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    """
    Validates password with complexity requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    - Contains special character
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@$!%*#?&]', password):
        return False
    return True

def is_valid_phone(phone_number):
    """
    Validates Kenyan phone numbers in international or local format.
    Examples: +254712345678, 0712345678
    """
    pattern = re.compile(r"^(\+254|0)[17]\d{8}$")
    return pattern.match(phone_number)
