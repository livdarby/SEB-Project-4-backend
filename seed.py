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

        users_data = [{
                "username": "admin",
                "email": "oliviadarby@live.co.uk",
                "password": "Admin1234!"
            },
            # {
            #     "username": "Liv",
            #     "email": "liv@me.com",
            #     "password": "Hello123!",
            #     "invite_code": "123",
            # },
            # {
            #     "username": "Lee",
            #     "email": "lee@me.com",
            #     "password": "Hello123!",
            #     "invite_code": "123",
            # }            
        ]

        for user_data in users_data:
            user = UserModel(**user_data)
            db.session.add(user)
        db.session.commit()

        def date_of_match(string):
            return datetime.strptime(string, "%a, %b %d %Y")

        matches_data = [
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Newcastle",
            #     "team_one_score": 4,
            #     "team_two_name": "Tottenham",
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Man City",
            #     "team_one_score": 5,
            #     "team_two_name": "Luton Town",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33 
            # },
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Burnley",
            #     "team_one_score": 1,
            #     "team_two_name": "Brighton",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" :33
            # },
            # {
            #     "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Liverpool",
            #     "team_one_score": 0,
            #     "team_two_name": "Crystal Palace",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33 
            # },
            # {
            #     "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Arsenal",
            #     "team_one_score": 0,
            #     "team_two_name": "Aston Villa",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Brentford",
            #     "team_one_score": 2,
            #     "team_two_name": "Sheffield United",
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Nottm Forest",
            #     "team_one_score": 2,
            #     "team_two_name": "Wolves",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sat, 13 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Bournemouth",
            #     "team_one_score": 2,
            #     "team_two_name": "Man United",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sun, 14 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "West Ham",
            #     "team_one_score": 0,
            #     "team_two_name": "Fulham",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Mon, 15 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Chelsea",
            #     "team_one_score": 6,
            #     "team_two_name": "Everton",
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 33
            # },
            # {
            #     "match_date": "Sat, 20 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Luton Town",
            #     "team_one_score": 1,
            #     "team_two_name": "Brentford",
            #     "team_two_score": 5,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 34
            # },
            # {
            #     "match_date": "Sat, 20 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Wolves",
            #     "team_one_score": 0,
            #     "team_two_name": "Arsenal",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" :34
            # },
            # {
            #     "match_date": "Sun, 21 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Crystal Palace",
            #     "team_one_score": 5,
            #     "team_two_name": "West Ham",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" :34
            # },
            # {
            #     "match_date": "Sun, 21 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Fulham",
            #     "team_one_score": 1,
            #     "team_two_name": "Liverpool",
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 34
            # },
            # {
            #     "match_date": "Sat, 20 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Sheffield United",
            #     "team_one_score": 1,
            #     "team_two_name": "Burnley",
            #     "team_two_score": 4,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 34
            # },
            # {
            #     "match_date": "Sun, 21 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Everton",
            #     "team_one_score": 2,
            #     "team_two_name": "Nottm Forest",
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 34
            # },
            # {
            #     "match_date": "Sun, 21 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Aston Villa",
            #     "team_one_score": 3,
            #     "team_two_name": "Bournemouth",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 34 
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Crystal Palace",
            #     "team_one_score": 2,
            #     "team_two_name": "Man City",
            #     "team_two_score": 4,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Wolves",
            #     "team_one_score": 1,
            #     "team_two_name": "West Ham",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Everton",
            #     "team_one_score": 1,
            #     "team_two_name": "Burnley",
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Aston Villa",
            #     "team_one_score": 3,
            #     "team_two_name": "Brentford",
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Fulham",
            #     "team_one_score": 0,
            #     "team_two_name": "Newcastle",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Luton Town",
            #     "team_one_score": 2,
            #     "team_two_name": "Bournemouth",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sat, 6 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Brighton",
            #     "team_one_score": 0,
            #     "team_two_name": "Arsenal",
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sun, 7 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Man United",
            #     "team_one_score": 2,
            #     "team_two_name": "Liverpool",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sun, 7 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Sheffield United",
            #     "team_one_score": 2,
            #     "team_two_name": "Chelsea",
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Sun, 7 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Tottenham",
            #     "team_one_score": 3,
            #     "team_two_name": "Nottm Forest",
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 32
            # },
            # {
            #     "match_date": "Tue, 23 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Arsenal",
            #     "team_one_score": None,
            #     "team_two_name": "Chelsea",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
            # {
            #     "match_date": "Wed, 24 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Wolves",
            #     "team_one_score": None,
            #     "team_two_name": "Bournemouth",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
            # {
            #     "match_date": "Wed, 24 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Crystal Palace",
            #     "team_one_score": None,
            #     "team_two_name": "Newcastle",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
            # {
            #     "match_date": "Wed, 24 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Man United",
            #     "team_one_score": None,
            #     "team_two_name": "Sheffield United",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
            # {
            #     "match_date": "Wed, 24 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Everton",
            #     "team_one_score": None,
            #     "team_two_name": "Liverpool",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
            # {
            #     "match_date": "Wed, 24 Apr 2024 00:00:00 GMT",
            #     "team_one_name": "Brighton",
            #     "team_one_score": None,
            #     "team_two_name": "Man City",
            #     "team_two_score": None,
            #     "date_created": datetime.now(timezone.utc),
            #     "match_week" : 29
            # },
        ]

        for match_data in matches_data:
            match = MatchModel(**match_data)
            db.session.add(match)
        db.session.commit()

        predictions_data = [
            # MATCH WEEK 33, USER 1, MATCH ID 1 - 10
            # { 
            #     "team_one_name": "Newcastle",
            #     "team_two_name": "Tottenham",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 1,
            # },
            # {
            #     "team_one_name": "Man City",
            #     "team_two_name": "Luton Town",
            #     "team_one_score": 3,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 2,
            # },
            # {
            #     "team_one_name": "Burnley",
            #     "team_two_name": "Brighton",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 3,
            # },
            # {
            #     "team_one_name": "Liverpool",
            #     "team_two_name": "Crystal Palace",
            #     "team_one_score": 0,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 4,
            # },
            # {
            #     "team_one_name": "Arsenal",
            #     "team_two_name": "Aston Villa",
            #     "team_one_score": 1,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 5,
            # },
            # {
            #     "team_one_name": "Brentford",
            #     "team_two_name": "Sheffield United",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 6,
            # },
            # {
            #     "team_one_name": "Nottm Forest",
            #     "team_two_name": "Wolves",
            #     "team_one_score": 4,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 7,
            # },
            # {
            #     "team_one_name": "Bournemouth",
            #     "team_two_name": "Man United",
            #     "team_one_score": 0,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 8,
            # },
            # {
            #     "team_one_name": "West Ham",
            #     "team_two_name": "Fulham",
            #     "team_one_score": 0,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 9,
            # },
            # {
            #     "team_one_name": "Chelsea",
            #     "team_two_name": "Everton",
            #     "team_one_score": 4,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 10,
            # },
            # #  MATCH WEEK 32, USER 1, MATCH ID 18 - 27
            # {
            #     "team_one_name": "Crystal Palace",
            #     "team_two_name": "Man City",
            #     "team_one_score": 0,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 18,
            # },
            # {
            #     "team_one_name": "Wolves",
            #     "team_two_name": "West Ham",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 19,
            # },
            # {
            #     "team_one_name": "Everton",
            #     "team_two_name": "Burnley",
            #     "team_one_score": 1,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 20,
            # },
            # {
            #     "team_one_name": "Aston Villa",
            #     "team_two_name": "Brentford",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 21,
            # },
            # {
            #     "team_one_name": "Fulham",
            #     "team_two_name": "Newcastle",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 22,
            # },
            # {
            #     "team_one_name": "Luton Town",
            #     "team_two_name": "Bournemouth",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 23,
            # },
            # {
            #     "team_one_name": "Brighton",
            #     "team_two_name": "Arsenal",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 24,
            # },
            # {
            #     "team_one_name": "Man United",
            #     "team_two_name": "Liverpool",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 25,
            # },
            # {
            #     "team_one_name": "Sheffield United",
            #     "team_two_name": "Chelsea",
            #     "team_one_score": 3,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 26,
            # },
            # {
            #     "team_one_name": "Tottenham",
            #     "team_two_name": "Nottm Forest",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 27,
            # },
            # # MATCH WEEK 33, USER 2, MATCH ID 1 - 10
            # {
            #     "team_one_name": "Newcastle",
            #     "team_two_name": "Tottenham",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 1,
            # },
            # {
            #     "team_one_name": "Man City",
            #     "team_two_name": "Luton Town",
            #     "team_one_score": 3,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 2,
            # },
            # {
            #     "team_one_name": "Burnley",
            #     "team_two_name": "Brighton",
            #     "team_one_score": 1,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 3,
            # },
            # {
            #     "team_one_name": "Liverpool",
            #     "team_two_name": "Crystal Palace",
            #     "team_one_score": 0,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 4,
            # },
            # {
            #     "team_one_name": "Arsenal",
            #     "team_two_name": "Aston Villa",
            #     "team_one_score": 1,
            #     "team_two_score": 4,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 5,
            # },
            # {
            #     "team_one_name": "Brentford",
            #     "team_two_name": "Sheffield United",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 6,
            # },
            # {
            #     "team_one_name": "Nottm Forest",
            #     "team_two_name": "Wolves",
            #     "team_one_score": 3,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 7,
            # },
            # {
            #     "team_one_name": "Bournemouth",
            #     "team_two_name": "Man United",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 8,
            # },
            # {
            #     "team_one_name": "West Ham",
            #     "team_two_name": "Fulham",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 9,
            # },
            # {
            #     "team_one_name": "Chelsea",
            #     "team_two_name": "Everton",
            #     "team_one_score": 6,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 10,
            # },
            # # MATCH WEEK 32, USER 2, MATCH ID 18 - 27
            # {
            #     "team_one_name": "Crystal Palace",
            #     "team_two_name": "Man City",
            #     "team_one_score": 0,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 18,
            # },
            # {
            #     "team_one_name": "Wolves",
            #     "team_two_name": "West Ham",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 19,
            # },
            # {
            #     "team_one_name": "Everton",
            #     "team_two_name": "Burnley",
            #     "team_one_score": 1,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 20,
            # },
            # {
            #     "team_one_name": "Aston Villa",
            #     "team_two_name": "Brentford",
            #     "team_one_score": 2,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 21,
            # },
            # {
            #     "team_one_name": "Fulham",
            #     "team_two_name": "Newcastle",
            #     "team_one_score": 3,
            #     "team_two_score": 4,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 22,
            # },
            # {
            #     "team_one_name": "Luton Town",
            #     "team_two_name": "Bournemouth",
            #     "team_one_score": 3,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 23,
            # },
            # {
            #     "team_one_name": "Brighton",
            #     "team_two_name": "Arsenal",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 24,
            # },
            # {
            #     "team_one_name": "Man United",
            #     "team_two_name": "Liverpool",
            #     "team_one_score": 1,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 25,
            # },
            # {
            #     "team_one_name": "Sheffield United",
            #     "team_two_name": "Chelsea",
            #     "team_one_score": 4,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 26,
            # },
            # {
            #     "team_one_name": "Tottenham",
            #     "team_two_name": "Nottm Forest",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 27,
            # },
            # # MATCH WEEK 34, USER 1, MATCH ID 11 - 17
            # {
            #     "team_one_name": "Luton Town",
            #     "team_two_name": "Brentford",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 11,
            # },
            # {
            #     "team_one_name": "Wolves",
            #     "team_two_name": "Arsenal",
            #     "team_one_score": 1,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 12,
            # },
            # {
            #     "team_one_name": "Crystal Palace",
            #     "team_two_name": "West Ham",
            #     "team_one_score": 3,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 13,
            # },
            # {
            #     "team_one_name": "Fulham",
            #     "team_two_name": "Liverpool",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 14,
            # },
            # {
            #     "team_one_name": "Sheffield United",
            #     "team_two_name": "Burnley",
            #     "team_one_score": 3,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 15,
            # },
            # {
            #     "team_one_name": "Everton",
            #     "team_two_name": "Nottm Forest",
            #     "team_one_score": 2,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 16,
            # },
            # {
            #     "team_one_name": "Aston Villa",
            #     "team_two_name": "Bournemouth",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 2,
            #     "match_id": 17,
            # },
            # # MATCH WEEK 34, USER 2, MATCH ID 11 - 17
            # {
            #     "team_one_name": "Luton Town",
            #     "team_two_name": "Brentford",
            #     "team_one_score": 1,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 11,
            # },
            # {
            #     "team_one_name": "Wolves",
            #     "team_two_name": "Arsenal",
            #     "team_one_score": 2,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 12,
            # },
            # {
            #     "team_one_name": "Crystal Palace",
            #     "team_two_name": "West Ham",
            #     "team_one_score": 1,
            #     "team_two_score": 3,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 13,
            # },
            # {
            #     "team_one_name": "Fulham",
            #     "team_two_name": "Liverpool",
            #     "team_one_score": 2,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 14,
            # },
            # {
            #     "team_one_name": "Sheffield United",
            #     "team_two_name": "Burnley",
            #     "team_one_score": 1,
            #     "team_two_score": 0,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 15,
            # },
            # {
            #     "team_one_name": "Everton",
            #     "team_two_name": "Nottm Forest",
            #     "team_one_score": 1,
            #     "team_two_score": 2,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 16,
            # },
            # {
            #     "team_one_name": "Aston Villa",
            #     "team_two_name": "Bournemouth",
            #     "team_one_score": 3,
            #     "team_two_score": 1,
            #     "date_created": datetime.now(timezone.utc),
            #     "user_id": 3,
            #     "match_id": 17,
            # },
            
        ]

        for prediction_data in predictions_data:
            prediction = PredictionModel(**prediction_data)
            db.session.add(prediction)
        db.session.commit()

        print("Seeding some data...")

    except Exception as e:
        print(e)
