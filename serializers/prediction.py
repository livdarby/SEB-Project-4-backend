from models.prediction import PredictionModel
from models.match import MatchModel
from app import marsh
from marshmallow import fields
from serializers.user import UserSerializer
from serializers.match import MatchSerializer

class PredictionSerializer(marsh.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer", many=False)
    match = fields.Nested("MatchSerializer", many=False)
    class Meta:
        model = PredictionModel
        load_instance = True