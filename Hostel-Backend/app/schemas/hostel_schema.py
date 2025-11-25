from marshmallow import Schema, fields, validates, ValidationError, validate
import json

class HostelCreateSchema(Schema):
    """Schema for hostel creation validation"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    location = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=10, max=2000))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    currency = fields.Str(required=False, default='KES', validate=validate.Length(max=3))
    capacity = fields.Int(required=True, validate=validate.Range(min=1, max=1000))
    
    # UPDATED: Added specific room types requested
    room_type = fields.Str(
        required=True,
        validate=validate.OneOf([
            'bedsitter', 'studio', '1_bedroom', '2_bedroom', '3_bedroom', 
            'single', 'double', 'triple', 'dormitory'
        ])
    )
    
    amenities = fields.List(fields.Int(), required=False, default=[])
    images = fields.List(fields.Str(), required=False, default=[], validate=validate.Length(max=6))
    latitude = fields.Float(required=False, allow_none=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=False, allow_none=True, validate=validate.Range(min=-180, max=180))
    
    # Features will accept arbitrary keys for rent_included, bathrooms, etc.
    features = fields.Dict(required=False, default={})
    is_verified = fields.Bool(required=False, default=False)
    is_featured = fields.Bool(required=False, default=False)

    @validates('amenities')
    def validate_amenities(self, value):
        if not isinstance(value, list):
            raise ValidationError('Amenities must be a list of integers')

    @validates('images')
    def validate_images(self, value):
        if len(value) > 6:
            raise ValidationError('Maximum 6 images allowed')
        for url in value:
            if not isinstance(url, str) or len(url) > 500:
                raise ValidationError('Invalid image URL')

# ... (Rest of the file remains the same)

class HostelUpdateSchema(Schema):
    """Schema for hostel update validation"""
    name = fields.Str(required=False, validate=validate.Length(min=2, max=200))
    location = fields.Str(required=False, validate=validate.Length(min=2, max=200))
    description = fields.Str(required=False, validate=validate.Length(min=10, max=2000))
    price = fields.Float(required=False, validate=validate.Range(min=0))
    currency = fields.Str(required=False, validate=validate.Length(max=3))
    capacity = fields.Int(required=False, validate=validate.Range(min=1, max=1000))
    room_type = fields.Str(
        required=False,
        validate=validate.OneOf(['single', 'double', 'triple', 'dormitory', 'apartment'])
    )
    amenities = fields.List(fields.Int(), required=False)
    images = fields.List(fields.Str(), required=False)
    latitude = fields.Float(required=False, allow_none=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=False, allow_none=True, validate=validate.Range(min=-180, max=180))
    features = fields.Dict(required=False)
    is_verified = fields.Bool(required=False)
    is_featured = fields.Bool(required=False)

    @validates('amenities')
    def validate_amenities(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError('Amenities must be a list of integers')
            if len(value) > 50:
                raise ValidationError('Too many amenities selected')

    @validates('images')
    def validate_images(self, value):
        if value is not None:
            if len(value) > 20:
                raise ValidationError('Too many images')
            for url in value:
                if not isinstance(url, str) or len(url) > 500:
                    raise ValidationError('Invalid image URL')

class HostelSearchSchema(Schema):
    """Schema for hostel search query parameters"""
    q = fields.Str(required=False, validate=validate.Length(max=100))
    location = fields.Str(required=False, validate=validate.Length(max=100))
    min_price = fields.Float(required=False, validate=validate.Range(min=0))
    max_price = fields.Float(required=False, validate=validate.Range(min=0))
    room_type = fields.List(fields.Str(
        validate=validate.OneOf(['single', 'double', 'triple', 'dormitory', 'apartment'])
    ), required=False)
    min_capacity = fields.Int(required=False, validate=validate.Range(min=1))
    amenities = fields.List(fields.Int(), required=False)
    furnished = fields.Bool(required=False)
    verified_only = fields.Bool(required=False)
    featured_only = fields.Bool(required=False)
    lat = fields.Float(required=False, validate=validate.Range(min=-90, max=90))
    lng = fields.Float(required=False, validate=validate.Range(min=-180, max=180))
    radius = fields.Float(required=False, validate=validate.Range(min=0.1, max=100))
    check_in = fields.Date(required=False)
    check_out = fields.Date(required=False)
    sort_by = fields.Str(
        required=False,
        validate=validate.OneOf(['price_asc', 'price_desc', 'rating', 'newest', 'relevance'])
    )
    page = fields.Int(required=False, default=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, default=20, validate=validate.Range(min=1, max=100))

class HostelListQuerySchema(Schema):
    """Schema for hostel list query parameters"""
    page = fields.Int(required=False, default=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, default=20, validate=validate.Range(min=1, max=100))
    location = fields.Str(required=False, validate=validate.Length(max=100))
    min_price = fields.Float(required=False, validate=validate.Range(min=0))
    max_price = fields.Float(required=False, validate=validate.Range(min=0))
    room_type = fields.List(fields.Str(
        validate=validate.OneOf(['single', 'double', 'triple', 'dormitory', 'apartment'])
    ), required=False)
    min_capacity = fields.Int(required=False, validate=validate.Range(min=1))
    amenities = fields.List(fields.Int(), required=False)
    furnished = fields.Bool(required=False)
    verified_only = fields.Bool(required=False)
    featured_only = fields.Bool(required=False)
    sort_by = fields.Str(
        required=False,
        validate=validate.OneOf(['price_asc', 'price_desc', 'rating', 'newest', 'relevance'])
    )

class AmenitySchema(Schema):
    """Schema for amenity validation"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    icon = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
