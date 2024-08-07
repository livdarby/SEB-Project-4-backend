from http import HTTPStatus
import logging
from datetime import datetime, timezone, timedelta
import pytz
import os
import pprint
from flask import Blueprint, g, request
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from serpapi import GoogleSearch
from config.environment import API_KEY


# Could we do a get to clean the data
# And a post to post this data to the db?
# Instead of doing it all in one controller?

# we need to check if a match already exists before posting it

from models.match import MatchModel
from models.prediction import PredictionModel
from middleware.secure_route import secure_route

from app import db
from serializers.match import MatchSerializer
from serializers.prediction import PredictionSerializer

router = Blueprint("matches", __name__)

match_serializer = MatchSerializer()
prediction_serializer = PredictionSerializer()


@router.route("/matches", methods=["GET"])
def get_matches():
    matches = MatchModel.query.all()
    # print(matches)
    return match_serializer.jsonify(matches, many=True), HTTPStatus.OK


@router.route("/match/<int:match_id>", methods=["GET"])
@secure_route
def get_match_by_id(match_id):
    match = db.session.query(MatchModel).get(match_id)
    if not match:
        return (
            {"message": "No match found. Provide a valid id"},
            HTTPStatus.NOT_FOUND,
        )
    return match_serializer.jsonify(match), HTTPStatus.OK


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
@secure_route
def create():

    match_dictionary = request.json
    match_model = match_serializer.load(match_dictionary)

    def check_if_match_existing(team_one_name, team_two_name):
        match = (
            db.session.query(MatchModel)
            .filter(
                func.lower(MatchModel.team_one_name) == func.lower(team_one_name),
                func.lower(MatchModel.team_two_name) == func.lower(team_two_name),
            )
            .first()
        )
        print(match)
        return match

    try:

        existing_match = check_if_match_existing(
            match_model.team_one_name, match_model.team_two_name
        )

        if existing_match:
            return {"message": "Match already exists."}, HTTPStatus.CONFLICT

        datetime_object = datetime.strptime(match_model.match_date, "%Y-%m-%dT%H:%M")
        formatted_string = datetime_object.strftime("%a, %d %b %Y %H:%M:%S")
        match_model.match_date = formatted_string
        match_model.date_created = datetime.now(timezone.utc)
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


@router.route("/scores", methods=["PUT"])
@secure_route
def update_score():
    try:

        # Get the match from the database using the two team names

        match_dictionary = request.json

        def check_match_exists(team_one_name, team_two_name):
            match = (
                db.session.query(MatchModel)
                .filter(
                    func.lower(MatchModel.team_one_name) == func.lower(team_one_name),
                    func.lower(MatchModel.team_two_name) == func.lower(team_two_name),
                )
                .first()
            )
            return match

        existing_match = check_match_exists(
            match_dictionary["team_one_name"], match_dictionary["team_two_name"]
        )

        if not existing_match:
            return {
                "message": "Match does not exist in the database"
            }, HTTPStatus.NOT_FOUND

        print(existing_match)

        existing_match.team_one_score = match_dictionary["team_one_score"]
        existing_match.team_two_score = match_dictionary["team_two_score"]

        db.session.commit()

        # Update the team_one_score and team_two_score of the found match

        return match_serializer.jsonify(existing_match), HTTPStatus.OK

    except ValidationError as e:
        return {"errors": e.messages}, HTTPStatus.BAD_REQUEST


@router.route("/matchesbyweek/<int:match_week>", methods=["GET"])
@secure_route
def get_matches_by_match_week(match_week):
    try:
        matches = db.session.query(MatchModel).all()
        matches_by_match_week = []
        for match in matches:
            if match.match_week == match_week:
                matches_by_match_week.append(match)
        print(matches_by_match_week)
        if not matches:
            return {"message": "No matches for the game week selected"}

        return match_serializer.jsonify(matches_by_match_week, many=True), HTTPStatus.OK
    except ValidationError as e:
        print(e.messages)
        return {"errors": e.messages}, HTTPStatus.BAD_REQUEST

    # Get all available match weeks!


@router.route("/matchweeks", methods=["GET"])
@secure_route
def get_match_weeks():
    try:
        matches = db.session.query(MatchModel).all()
        match_weeks = []
        for match in matches:
            match_weeks.append(match.match_week)
        match_weeks = list(dict.fromkeys(match_weeks))
        print(match_weeks)
        return match_weeks
    except ValidationError as e:
        return {"errors": e.messages}, HTTPStatus.BAD_REQUEST

