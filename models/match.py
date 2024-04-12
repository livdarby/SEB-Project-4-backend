from app import db


class MatchModel(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    team_one_name = db.Column(db.Text, nullable=False)
    team_two_name = db.Column(db.Text, nullable=False)
    team_one_score = db.Column(db.Integer, nullable=True)
    team_two_score = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.Text, nullable=True)
    match_date = db.Column(db.Text, nullable=False)
    # prediction_id = db.Column(db.Integer, db.ForeignKey("predictions.id"), nullable=True)

    # prediction = db.relationship("PredictionModel", backref="predictions")
