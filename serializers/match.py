from app import marsh
from models.match import MatchModel

class MatchSerializer(marsh.SQLAlchemyAutoSchema):

    class Meta:
        model = MatchModel
        load_instance = True