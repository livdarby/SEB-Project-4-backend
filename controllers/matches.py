from http import HTTPStatus
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, g
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError

from models.match import MatchModel
from middleware.secure_route import secure_route

from app import db
from serializers.match import MatchSerializer

router = Blueprint("matches", __name__)

match_serializer = MatchSerializer()

@router.route("/matches", methods=["GET"])
def get_matches():
    matches = MatchModel.query.all()
    print(matches)
    return match_serializer.jsonify(matches, many=True), HTTPStatus.OK


@router.route("/matches", methods=["POST"])
@secure_route
def create():

    def date_of_match(string):
        return datetime.strptime(string, "%a, %b %d").replace(year=datetime.now().year)

    match_dictionary = request.json
    try:
        match_model = match_serializer.load(match_dictionary)
        match_model.match_date = date_of_match(match_model.match_date)
        match_model.date_created = datetime.now(timezone.utc)
        print(match_model.match_date)
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
