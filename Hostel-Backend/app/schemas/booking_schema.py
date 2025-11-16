from marshmallow import Schema, fields, validates, ValidationError, validate
from datetime import datetime, date

class BookingCreateSchema(Schema):
    """Schema for booking creation validation"""
    hostel_id = fields.Int(required=True, validate=validate.Range(min=1))
    check_in = fields.Date(required=True)
    check_out = fields.Date(required=True)
    guests = fields.Int(required=True, validate=validate.Range(min=1, max=20))
    phone_number = fields.Str(required=True)

    @validates('check_in')
    def validate_check_in(self, value):
        if value <= date.today():
            raise ValidationError('Check-in date must be in the future')

    @validates('check_out')
    def validate_check_out(self, value, **kwargs):
        check_in = kwargs.get('check_in')
        if check_in and value <= check_in:
            raise ValidationError('Check-out date must be after check-in date')

    @validates('phone_number')
    def validate_phone(self, value):
        # Basic phone validation - should be enhanced based on requirements
        if not value or len(value) < 10:
            raise ValidationError('Invalid phone number')

class BookingUpdateSchema(Schema):
    """Schema for booking update validation (admin/landlord only)"""
    status = fields.Str(
        required=True,
        validate=validate.OneOf(['confirmed', 'cancelled', 'completed', 'no_show'])
    )

class BookingListQuerySchema(Schema):
    """Schema for booking list query parameters"""
    page = fields.Int(required=False, default=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, default=20, validate=validate.Range(min=1, max=100))
    status = fields.Str(
        required=False,
        validate=validate.OneOf(['confirmed', 'upcoming', 'completed', 'cancelled', 'no_show'])
    )

class PaymentInitiateSchema(Schema):
    """Schema for payment initiation validation"""
    phone_number = fields.Str(required=True)

    @validates('phone_number')
    def validate_phone(self, value):
        # Basic phone validation for M-Pesa
        if not value or len(value) < 10:
            raise ValidationError('Invalid phone number for payment')

class ReviewCreateSchema(Schema):
    """Schema for review creation validation"""
    hostel_id = fields.Int(required=True, validate=validate.Range(min=1))
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, allow_none=True, validate=validate.Length(max=1000))

class ReviewUpdateSchema(Schema):
    """Schema for review update validation"""
    rating = fields.Int(required=False, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, allow_none=True, validate=validate.Length(max=1000))

class ContactFormSchema(Schema):
    """Schema for contact form validation"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    subject = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    message = fields.Str(required=True, validate=validate.Length(min=10, max=2000))

class SearchSuggestionsSchema(Schema):
    """Schema for search suggestions query"""
    q = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    limit = fields.Int(required=False, default=10, validate=validate.Range(min=1, max=20))

class PopularLocationsSchema(Schema):
    """Schema for popular locations query"""
    limit = fields.Int(required=False, default=20, validate=validate.Range(min=1, max=50))
