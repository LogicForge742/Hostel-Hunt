from marshmallow import Schema, fields, validates, ValidationError, validate
from ..utils.validator import is_valid_email, is_valid_password, is_valid_phone

class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    phone_number = fields.Str(required=False, allow_none=True)
    role = fields.Str(
        required=False,
        validate=validate.OneOf(['student', 'landlord']),
        default='student'
    )

    @validates('email')
    def validate_email(self, value):
        if not is_valid_email(value):
            raise ValidationError('Invalid email address')

    @validates('password')
    def validate_password_strength(self, value):
        if not is_valid_password(value):
            raise ValidationError('Password must be at least 8 characters with uppercase, lowercase, number, and special character')

    @validates('phone_number')
    def validate_phone(self, value):
        if value and not is_valid_phone(value):
            raise ValidationError('Invalid phone number format')

class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))

class UserProfileUpdateSchema(Schema):
    """Schema for user profile update validation"""
    name = fields.Str(required=False, validate=validate.Length(min=2, max=100))
    phone_number = fields.Str(required=False, allow_none=True)
    profile_image = fields.Str(required=False, allow_none=True)

    @validates('phone_number')
    def validate_phone(self, value):
        if value and not is_valid_phone(value):
            raise ValidationError('Invalid phone number format')

class ChangePasswordSchema(Schema):
    """Schema for password change validation"""
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6, max=128))

    @validates('new_password')
    def validate_password_strength(self, value):
        if not is_valid_password(value):
            raise ValidationError('Password must be at least 8 characters with uppercase, lowercase, number, and special character')

class LandlordProfileSchema(Schema):
    """Schema for landlord profile creation/update validation"""
    business_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    contact_phone = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=1000))

    @validates('contact_email')
    def validate_contact_email(self, value):
        if not is_valid_email(value):
            raise ValidationError('Invalid contact email address')

    @validates('contact_phone')
    def validate_contact_phone(self, value):
        if not is_valid_phone(value):
            raise ValidationError('Invalid contact phone number')

class UserRoleUpdateSchema(Schema):
    """Schema for admin user role update validation"""
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['student', 'landlord', 'admin'])
    )

class UserListQuerySchema(Schema):
    """Schema for user list query parameters"""
    page = fields.Int(required=False, default=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, default=20, validate=validate.Range(min=1, max=100))
    role = fields.Str(required=False, validate=validate.OneOf(['student', 'landlord', 'admin']))
    is_active = fields.Bool(required=False)
    email_verified = fields.Bool(required=False)
