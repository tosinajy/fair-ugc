from marshmallow import Schema, fields, validate

class CalculationSchema(Schema):
    content_type = fields.Str(
        required=True, 
        validate=validate.OneOf(["video", "photo", "testimonial"], error="Invalid content type selected.")
    )
    experience_level = fields.Str(
        required=True,
        validate=validate.OneOf(["beginner", "intermediate", "pro"], error="Invalid experience level.")
    )
    niche = fields.Str(required=True, validate=validate.Length(min=1))
    # Validates that usage_rights is a list of strings
    usage_rights = fields.List(fields.Str(), missing=[])

class LeadSchema(Schema):
    email = fields.Email(required=True, error_messages={"invalid": "Not a valid email address."})

class RoleSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    permissions = fields.List(fields.Int(), missing=[])

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role_id = fields.Int(required=True)