from http import HTTPStatus
import logging
from datetime import datetime, timezone, timedelta
import os
import pprint
from flask import Blueprint, g, request
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError
from serpapi import GoogleSearch
from config.environment import API_KEY

# Could we do a get to clean the data
# And a post to post this data to the db?
# Instead of doing it all in one controller?

# we need to check if a match already exists before posting it

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


@router.route("/new/matches/<club_name>", methods=["GET"])
def get_new_matches(club_name):

    premier_league_matches = []

    def fetch_matches():
        params = {
            "q": club_name,
            "api_key": API_KEY,
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        matches = results.get("sports_results", {})
        matches_games = matches.get("games", [])

        matches_spotlight = matches.get("game_spotlight")

        a = []

        if matches_spotlight:
            a.append(matches_spotlight.copy())

        matches = matches_games + a
        pprint.pp(matches)

        premier_league_matches = [
            match
            for match in matches
            if match.get("tournament") == "Premier League"
            or match.get("league") == "Premier League"
        ]
        return premier_league_matches

    premier_league_matches = fetch_matches()

    def formatted_date(string):
        if "yesterday" in string or "Yesterday" in string:
            return datetime.now(timezone.utc) - (timedelta(days=1))
        if "today" in string:
            return datetime.now(timezone.utc)
        elif "," in string:
            return datetime.strptime(string, "%a, %b %d").replace(
                year=datetime.now().year
            )
        return datetime.strptime(string, "%b %d").replace(year=datetime.now().year)

    filtered_matches = []
    for match in premier_league_matches:

        filtered_teams = []

        for team in match["teams"]:
            team_info = {"name": team["name"]}
            if "score" in team:
                team_info["score"] = team["score"]
            filtered_teams.append(team_info)

        filtered_match = {
            "date": formatted_date(match["date"]),
            "teams": filtered_teams,
        }
        filtered_matches.append(filtered_match)

    return filtered_matches, HTTPStatus.OK


@router.route("/matches", methods=["POST"])
# @secure_route
def create():

    match_dictionary = request.json

    def check_if_match_existing(team_one_name, team_two_name):
        match = db.session.query(MatchModel).filter(MatchModel.team_one_name == team_one_name, MatchModel.team_two_name == team_two_name).first()
        return match

    try:
        for match in match_dictionary:

            # we need some logic to check if each object in match['teams'] contains a key 'score'
            # if yes, we need to assign the value to team_one_score and team_two_score
            # if not, the scores should be None
            filtered_scores = []

            for team in match["teams"]:  # here, we have identified each team object
                if "score" in team:
                    filtered_scores.append(int(team["score"]))

            if filtered_scores:
                team_one_score = filtered_scores[0]
                team_two_score = filtered_scores[1]
            else:
                team_one_score = None
                team_two_score = None

            match_model = match_serializer.load(
                {
                    "match_date": match["date"],
                    "date_created": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "team_one_name": match["teams"][0]["name"],
                    "team_one_score": team_one_score,
                    "team_two_score": team_two_score,
                    "team_two_name": match["teams"][1]["name"],
                }
            )
            # we need to check whether the match already exists in the db
            # take team_one_name and team_two_name and sort alphabetically
            # check if they already exist in the db

            existing_match = check_if_match_existing(match_model.team_one_name, match_model.team_two_name)
            if existing_match:
                pass
            else:
                db.session.add(match_model)
                db.session.commit()

            # db.session.add(match_model)

        return {"message": "Matches successfully posted to the db"}, HTTPStatus.OK

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
