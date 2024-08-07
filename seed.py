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
                "password": "Admin1234!",
                "permissions" : "admin"
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

        # matches_data = [
        # ]

        # for match_data in matches_data:
        #     match = MatchModel(**match_data)
        #     db.session.add(match)
        # db.session.commit()

        # predictions_data = [
        # ]

        # for prediction_data in predictions_data:
        #     prediction = PredictionModel(**prediction_data)
        #     db.session.add(prediction)
        # db.session.commit()

        print("Seeding some data...")

    except Exception as e:
        print(e)
