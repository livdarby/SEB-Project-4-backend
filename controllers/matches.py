from http import HTTPStatus
import logging
from datetime import datetime, timezone
import os
import pprint
from flask import Blueprint, g
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Could we do a get to clean the data
# And a post to post this data to the db?
# Instead of doing it all in one controller?

load_dotenv()
api_key = os.getenv("API_KEY")

from models.match import MatchModel
from middleware.secure_route import secure_route

from app import db
from serializers.match import MatchSerializer

router = Blueprint("matches", __name__)

match_serializer = MatchSerializer()


@router.route("/matches", methods=["GET"])
def get_matches():
    matches = MatchModel.query.all()
    # print(matches)
    return match_serializer.jsonify(matches, many=True), HTTPStatus.OK


@router.route("/matches", methods=["POST"])
@secure_route
def create():

    premier_league_clubs = [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton & Hove Albion",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Liverpool",
        "Luton Town",
        "Manchester City",
        "Manchester United",
        "Newcastle United",
        "Nottingham Forest",
        "Sheffield United",
        "Tottenham Hotspur",
        "West Ham United",
        "Wolverhampton Wanderers",
    ]

    def fetch_matches(club):
        params = {
            "q": club,
            # "location": "united kingdom",
            "api_key": api_key,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "sports_matches" in results.keys():
            matches = results["sports_results"]["games"]

            # pprint.pp(matches)
            premier_league_matches = [
                match for match in matches if match["tournament"] == "Premier League"
            ]
            # pprint.pp(premier_league_matches)
            for element in premier_league_matches:
                date = element["date"]
                teams = element["teams"]
                team_one = teams[0]["name"]
                team_two = teams[1]["name"]
                if "score" in teams[0].keys():
                    team_one_score = teams[0]["score"]
                    team_two_score = teams[1]["score"]
            return (date, team_one, team_two)

    def date_of_match(string):
        if (
            "Mon" in string
            or "Tue" in string
            or "Wed" in string
            or "Thu" in string
            or "Fri" in string
            or "Sat" in string
            or "Sun" in string
        ):
            return datetime.strptime(string, "%a, %b %d").replace(
                year=datetime.now().year
            )
        else:
            return datetime.strptime(string, "%b %d").replace(year=datetime.now().year)

    # match_dictionary = request.json

    try:
        for club in premier_league_clubs:
            data = fetch_matches(club)

            # print(data)
            date = data[0]
            team_one = data[1]
            team_two = data[2]

            # check if there is a score and if so, input into the api

            date_created = str(datetime.now(timezone.utc))
            match_date = str(date_of_match(date))
            # print(type(date_created), type(match_date))

            match_model = match_serializer.load(
                {
                    "match_date": match_date,
                    "date_created": date_created,
                    "team_one_name": team_one,
                    "team_two_name": team_two,
                }
            )
            # print(match_model.match_date)
            db.session.add(match_model)
            db.session.commit()
        return match_serializer.jsonify(match_model), HTTPStatus.OK

    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Please check the required fields and try again.",
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except SQLAlchemyError as e:
        print(e)

        class AppError(Exception):
            pass

        class matchSchema(Schema):
            name = fields.String()

            def handle_error(self, error, data, **kwargs):
                logging.error(error.messages)
                print(error.messages)
                raise AppError(f"An error occurred with input: {0}".format(data))

        schema = matchSchema()
        return (
            schema.load({"name": "Invalid name. Try again ❌"}),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
