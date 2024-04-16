from app import marsh
from models.user import UserModel
from marshmallow import fields, ValidationError

def validate_password(password):
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long")
    

class UserSerializer(marsh.SQLAlchemyAutoSchema):
    password = fields.String(required = True, validate=validate_password)
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password_hash", "email", "password")