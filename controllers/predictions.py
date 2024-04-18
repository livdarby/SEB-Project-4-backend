from http import HTTPStatus
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, g
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError

from models.prediction import PredictionModel
from models.match import MatchModel
from models.user import UserModel
from middleware.secure_route import secure_route

from app import db
from serializers.prediction import PredictionSerializer

router = Blueprint("predictions", __name__)

prediction_serializer = PredictionSerializer()


@router.route("/predictions", methods=["GET"])
def get_predictions():
    predictions = PredictionModel.query.all()
    return prediction_serializer.jsonify(predictions, many=True), HTTPStatus.OK


@router.route("/predictions", methods=["POST"])
@secure_route
def create():
    prediction_dictionary = request.json
    print(prediction_dictionary)

    try:
        match_id = prediction_dictionary.get("match")
        print(match_id["id"])
        found_match = db.session.query(MatchModel).get(match_id["id"])
        print('found: ', found_match)
        print(g.current_user)
        prediction_model = prediction_serializer.load(prediction_dictionary)
        prediction_model.user_id = g.current_user.id
        prediction_model.date_created = datetime.now(timezone.utc)
        prediction_model.match_id = found_match.id
        db.session.add(prediction_model)
        db.session.commit()
        return prediction_serializer.jsonify(prediction_model), HTTPStatus.OK
    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Please check the required fields and try again.",
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except SQLAlchemyError:

        class AppError(Exception):
            pass

        class predictionSchema(Schema):
            name = fields.String()

            def handle_error(self, error, data, **kwargs):
                logging.error(error.messages)
                raise AppError(f"An error occurred with input: {0}".format(data))

        schema = predictionSchema()
        return (
            schema.load({"name": "Invalid name. Try again ❌"}),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )


@router.route("/predictions/<int:user_id>", methods=["GET"])
@secure_route
def get_all_user_predictions(user_id):
    user = db.session.query(UserModel).get(user_id)
    if not user:
        return (
            {"message": "No user found. Provide a valid id"},
            HTTPStatus.NOT_FOUND,
        )
    if user.id != g.current_user.id:
        return {
            "message": "You are not authorised to get these predictions"
        }, HTTPStatus.UNAUTHORIZED
    predictions = db.session.query(PredictionModel).filter(
        PredictionModel.user_id == user.id
    )
    print(prediction_serializer.jsonify(predictions, many=True))
    return prediction_serializer.jsonify(predictions, many=True), HTTPStatus.OK

@router.route("/predictions/<int:prediction_id>", methods=["PUT"])
@secure_route
def editPrediction(prediction_id):
    try:
        prediction = db.session.query(PredictionModel).get(prediction_id)
        prediction_dictionary = request.json
        edited_prediction = prediction_serializer.load(prediction_dictionary, instance=prediction, partial=True)
        db.session.add(edited_prediction)
        db.session.commit()
        return prediction_serializer.jsonify(edited_prediction)
    except SQLAlchemyError as e:
        return {"errors" : e.messages, "message": "There has been an error"}