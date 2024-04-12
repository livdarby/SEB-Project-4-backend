from app import marsh
from models.user import UserModel
from marshmallow import fields

class UserSerializer(marsh.SQLAlchemyAutoSchema):
    password = fields.String(required = True)
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password_hash", "email", "password")