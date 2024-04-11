from app import db
from models.user import UserModel
from models.match import MatchModel

class PredictionModel(db.Model):
    __tablename__ = "predictions"
    id = db.Column(db.Integer, primary_key=True)
    team_one_score = db.Column(db.Integer, nullable = False)
    team_two_score = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.Text, nullable=False)    
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", backref="predictions")
    match = db.relationship("MatchModel", backref="matches")
