from datetime import datetime, timezone
from app import app, db
from models.prediction import PredictionModel
from models.user import UserModel
from models.match import MatchModel

with app.app_context():

    try: 
        print("Connected to the database! 🔥")
        db.drop_all()
        db.create_all()

        admin_user = UserModel(username = "Liv", email = "liv@me.com", password = "Hello123!", invite_code = "123")
        db.session.add(admin_user)
        db.session.commit()

        test_match = MatchModel(
            team_one_score = 2,
            team_two_score = 1,
            match_date = "6th April 2024",
            date_created = datetime.now(timezone.utc)
        )
        db.session.add(test_match)
        db.session.commit()

        test_prediction = PredictionModel(
            team_one_score = 1,
            team_two_score = 3,
            date_created = datetime.now(timezone.utc),
            user_id = admin_user.id,
            match_id = test_match.id
        )
        db.session.add(test_prediction)
        db.session.commit()

        print("Seeding some data...")
    
    except Exception as e:
        print(e)