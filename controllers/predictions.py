from http import HTTPStatus
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, g, jsonify
from marshmallow import ValidationError, Schema, fields
from sqlalchemy.exc import SQLAlchemyError

from models.prediction import PredictionModel
from models.match import MatchModel
from models.user import UserModel
from middleware.secure_route import secure_route

from app import db
from serializers.prediction import PredictionSerializer
from serializers.user import UserSerializer

router = Blueprint("predictions", __name__)

prediction_serializer = PredictionSerializer()
user_serializer = UserSerializer()


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
        print("found: ", found_match)
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
    # if user.id != g.current_user.id:
    #     return {
    #         "message": "You are not authorised to get these predictions"
    #     }, HTTPStatus.UNAUTHORIZED
    predictions = db.session.query(PredictionModel).filter(
        PredictionModel.user_id == user.id
    )
    print(prediction_serializer.jsonify(predictions, many=True))
    return prediction_serializer.jsonify(predictions, many=True), HTTPStatus.OK


@router.route("/checkpredictions/<int:user_id>", methods=["GET"])
@secure_route
def check_user_predictions(user_id):
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
    todays_date = datetime.now(timezone.utc)
    filtered_predictions = []
    for prediction in predictions:
        if (
            datetime.strptime(
                prediction.match.match_date, "%a, %d %b %Y %H:%M:%S %Z"
            ).replace(tzinfo=timezone.utc)
            < todays_date
        ):
            filtered_predictions.append(prediction)

    total_points = []
    for prediction in filtered_predictions:

        if (
            prediction.team_one_score == prediction.match.team_one_score
            and prediction.team_two_score == prediction.match.team_two_score
        ):
            total_points.append(3)
        elif (
            prediction.team_one_score == prediction.team_two_score
            and prediction.match.team_one_score == prediction.match.team_two_score
        ):
            total_points.append(1)
        elif (
            prediction.team_one_score < prediction.team_two_score
            and prediction.match.team_one_score < prediction.match.team_two_score
        ):
            total_points.append(1)
        elif (
            prediction.team_one_score > prediction.team_two_score
            and prediction.match.team_one_score > prediction.match.team_two_score
        ):
            total_points.append(1)
        print(total_points)
    print(total_points, filtered_predictions)
    sum_points = sum(total_points)
    print((sum_points))

    return (
        {"message": sum_points},
        HTTPStatus.OK,
    )


@router.route("/predictionresult/<int:prediction_id>")
@secure_route
def check_prediction(prediction_id):
    try:
        prediction = db.session.query(PredictionModel).get(prediction_id)
        matches = MatchModel.query.all()
        filtered_matches = []
        for match in matches:
            if match.id == prediction.match.id:
                filtered_matches.append(match)
        match = filtered_matches[0]
        print(prediction, match)
        if (
            prediction.team_one_score == match.team_one_score
            and prediction.team_two_score == match.team_two_score
        ):
            points = 3
        elif (
            prediction.team_one_score == prediction.team_two_score
            and match.team_one_score == match.team_two_score
        ):
            points = 1
        elif (
            prediction.team_one_score > prediction.team_two_score
            and match.team_one_score > match.team_two_score
        ):
            points = 1
        elif (
            prediction.team_one_score < prediction.team_two_score
            and match.team_one_score < match.team_two_score
        ):
            points = 1
        else:
            points = 0
        return {"points": points}, HTTPStatus.OK
    except SQLAlchemyError:
        return {"message": "There has been an error"}


@router.route("/predictions/<int:prediction_id>", methods=["PUT"])
@secure_route
def editPrediction(prediction_id):
    try:
        prediction = db.session.query(PredictionModel).get(prediction_id)
        prediction_dictionary = request.json
        edited_prediction = prediction_serializer.load(
            prediction_dictionary, instance=prediction, partial=True
        )
        db.session.add(edited_prediction)
        db.session.commit()
        return prediction_serializer.jsonify(edited_prediction)
    except SQLAlchemyError as e:
        return {"errors": e.messages, "message": "There has been an error"}


@router.route("/admin", methods=["POST"])
@secure_route
def postAdminPrediction():
    try:
        prediction_dictionary = request.json
        username = prediction_dictionary.pop("username", None)
        user = UserModel.query.filter_by(username=username).first()
        # print(prediction_dictionary["team_one_name"])
        if user:
            found_match = MatchModel.query.filter_by(
                team_one_name=prediction_dictionary["team_one_name"]
            ).first()
            if not found_match:
                return {"message": "Match not found"}, HTTPStatus.NOT_FOUND
            if found_match.team_two_name != prediction_dictionary["team_two_name"]:
                return {"message": "Match not found"}, HTTPStatus.NOT_FOUND
            print("found: ", found_match)
            predictions = PredictionModel.query.all()
            predictions_by_user = []
            for prediction in predictions:
                if prediction.user_id == user.id:
                    predictions_by_user.append(prediction)
            for prediction in predictions_by_user:
                if (
                    prediction.team_one_name == prediction_dictionary["team_one_name"]
                    and prediction.team_two_name
                    == prediction_dictionary["team_two_name"]
                ):
                    return {
                        "message": "Prediction already submitted"
                    }, HTTPStatus.CONFLICT
            prediction_model = prediction_serializer.load(prediction_dictionary)
            prediction_model.user_id = user.id
            prediction_model.date_created = datetime.now(timezone.utc)
            prediction_model.match_id = found_match.id
            db.session.add(prediction_model)
            db.session.commit()
            return prediction_serializer.jsonify(prediction_model), HTTPStatus.OK
        else:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND
    except SQLAlchemyError as e:
        return {
            "errors": e.messages,
            "message": "There has been an error",
        }, HTTPStatus.INTERNAL_SERVER_ERROR


@router.route("/prediction_by_user_and_match/<int:match_id>/<int:user_id>", methods=["GET"])
@secure_route
def get_predictions_by_user_and_match(match_id, user_id):
    try:
        predictions = db.session.query(PredictionModel).all()
        predictions_by_match_id = []
        for prediction in predictions:
            print(prediction.match.id)
            if prediction.match.id == match_id and prediction.user.id == user_id:
                predictions_by_match_id.append(prediction)
        if len(predictions_by_match_id) == 0:
            return {"messages": "No predictions for this match"}, HTTPStatus.OK
        return (
            prediction_serializer.jsonify(predictions_by_match_id, many=True),
            HTTPStatus.OK,
        )
    except ValidationError as e:
        return {"errors": e.messages}, HTTPStatus.NOT_FOUND
