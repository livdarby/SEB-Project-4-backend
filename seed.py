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

        user_one = UserModel(
            username="Liv", email="liv@me.com", password="Hello123!", invite_code="123"
        )
        db.session.add(user_one)
        db.session.commit()

        def date_of_match(string):
            return datetime.strptime(string, "%a, %b %d %Y")

        matches_data = [
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Newcastle",
                "team_one_score": 4,
                "team_two_name": "Tottenham Hotspur",
                "team_two_score": 0,
            },
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Manchester City",
                "team_one_score": 5,
                "team_two_name": "Luton Town",
                "team_two_score": 1,
            },
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Burnley",
                "team_one_score": 1,
                "team_two_name": "Brighton",
                "team_two_score": 1,
            },
            {
                "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
                "team_one_name": "Liverpool",
                "team_one_score": 0,
                "team_two_name": "Crystal Palace",
                "team_two_score": 1,
            },
            {
                "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
                "team_one_name": "Arsenal",
                "team_one_score": 0,
                "team_two_name": "Aston Villa",
                "team_two_score": 2,
            },
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Brentford",
                "team_one_score": 2,
                "team_two_name": "Sheffield United",
                "team_two_score": 0,
            },
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Nottingham Forest",
                "team_one_score": 2,
                "team_two_name": "Wolverhampton Wanderers",
                "team_two_score": 2,
            },
            {
                "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
                "team_one_name": "Bournemouth",
                "team_one_score": 2,
                "team_two_name": "Manchester United",
                "team_two_score": 2,
            },
            {
                "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
                "team_one_name": "West Ham United",
                "team_one_score": 0,
                "team_two_name": "Fulham",
                "team_two_score": 2,
            },
            {
                "match_date": "Mon, 15 Apr 2024 00:00:00 GMT",
                "team_one_name": "Chelsea",
                "team_one_score": 6,
                "team_two_name": "Everton",
                "team_two_score": 0,
            },
        ]

        for match_data in matches_data:
            match = MatchModel(**match_data)
            db.session.add(match)
        db.session.commit()

        predictions_data = [
            {
                "team_one_name": "Newcastle",
                "team_two_name": "Tottenham Hotspur",
                "team_one_score": 2,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":1,
            }, 
            {
                "team_one_name": "Manchester City",
                "team_two_name": "Luton Town",
                "team_one_score": 3,
                "team_two_score": 0,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":2,
            }, 
            {
                "team_one_name": "Burnley",
                "team_two_name": "Brighton",
                "team_one_score": 1,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":3,
            }, 
            {
                "team_one_name": "Liverpool",
                "team_two_name": "Crystal Palace",
                "team_one_score": 0,
                "team_two_score": 2,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":4,
            }, 
            {
                "team_one_name": "Arsenal",
                "team_two_name": "Aston Villa",
                "team_one_score": 1,
                "team_two_score": 3,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":5,
            }, 
            {
                "team_one_name": "Brentford",
                "team_two_name": "Sheffield United",
                "team_one_score": 1,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":6,
            }, 
            {
                "team_one_name": "Nottingham Forest",
                "team_two_name": "Wolverhampton Wanderers",
                "team_one_score": 4,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":7,
            }, 
            {
                "team_one_name": "Bournemouth",
                "team_two_name": "Manchester United",
                "team_one_score": 0,
                "team_two_score": 2,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":8,
            }, 
            {
                "team_one_name": "West Ham United",
                "team_two_name": "Fulham",
                "team_one_score": 0,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":9,
            }, 
            {
                "team_one_name": "Chelsea",
                "team_two_name": "Everton",
                "team_one_score": 4,
                "team_two_score": 1,
                "date_created": datetime.now(timezone.utc),
                "user_id": user_one.id,
                "match_id":10,
            }, 
        ]

        for prediction_data in predictions_data:
            prediction = PredictionModel(**prediction_data)
            db.session.add(prediction)
        db.session.commit()

        print("Seeding some data...")

    except Exception as e:
        print(e)
