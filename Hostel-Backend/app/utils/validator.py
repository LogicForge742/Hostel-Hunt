import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 6

def is_valid_phone(phone_number):
    """
    Validates phone numbers in international or local format.
    Examples: +254712345678, 0712345678
    """
    pattern = re.compile(r"^(\+\d{1,3})?\d{9,12}$")
    return pattern.match(phone_number)
