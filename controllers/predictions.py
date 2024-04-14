from http import HTTPStatus
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, g
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError

from models.prediction import PredictionModel
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

    try:
        prediction_model = prediction_serializer.load(prediction_dictionary)
        prediction_model.user_id = g.current_user.id
        prediction_model.date_created = datetime.now(timezone.utc)
        prediction_model.match_id = 1
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
