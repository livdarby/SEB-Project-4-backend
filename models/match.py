from app import db

class MatchModel(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    team_one_score = db.Column(db.Integer, nullable = False)
    team_two_score = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.Text, nullable=False)    
    match_date = db.Column(db.Text, nullable=False)
    # prediction_id = db.Column(db.Integer, db.ForeignKey("predictions.id"), nullable=True)

    # prediction = db.relationship("PredictionModel", backref="predictions")