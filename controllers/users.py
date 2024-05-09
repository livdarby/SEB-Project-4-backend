from http import HTTPStatus
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError
from serializers.user import UserSerializer
from config.environment import SECRET
from flask import Blueprint, request, g
import jwt
from marshmallow import ValidationError
from app import db
from models.user import UserModel
from models.prediction import PredictionModel
from models.match import MatchModel
from middleware.secure_route import secure_route

user_serializer = UserSerializer()

router = Blueprint("users", __name__)


@router.route("/signup", methods=["POST"])
def signup():
    try:
        user_dictionary = request.json
        user_model = user_serializer.load(user_dictionary)
        db.session.add(user_model)
        db.session.commit()
        return user_serializer.jsonify(user_model), HTTPStatus.OK

    except ValidationError as e:
        print(e)
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    except SQLAlchemyError:
        return {
            "message": "Please try again",
        }, HTTPStatus.UNPROCESSABLE_ENTITY


@router.route("/login", methods=["POST"])
def login():
    credentials_dictionary = request.json
    user = (
        db.session.query(UserModel)
        .filter_by(email=credentials_dictionary["email"])
        .first()
    )
    print(user)
    if not user:
        return {"message": "Login failed"}, HTTPStatus.NOT_FOUND

    if not user.validate_password(credentials_dictionary["password"]):
        return {"message": "Login failed"}, HTTPStatus.NOT_FOUND

    print("Login success!!! ✅")
    payload = {
        "exp": datetime.now(timezone.utc) + (timedelta(days=1)),
        "iat": datetime.now(timezone.utc),
        "sub": user.id,
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"message": "Log in successful 🏃‍♀️", "token": token}, HTTPStatus.OK


@router.route("/user", methods=["GET"])
@secure_route
def get_current_user():
    user = g.current_user.id
    if not user:
        return {"message": "Log in to continue"}, HTTPStatus.UNAUTHORIZED
    current_user = db.session.query(UserModel).get(user)
    return user_serializer.jsonify(current_user), HTTPStatus.OK


@router.route("/user/<int:user_id>", methods=["PUT"])
@secure_route
def edit_user(user_id):
    try:
        user = g.current_user.id
        if not user:
            return {"message": "Log in to continue"}, HTTPStatus.UNAUTHORIZED
        current_user = db.session.query(UserModel).get(user)
        user_dictionary = request.json
        user = user_serializer.load(
            user_dictionary, instance=current_user, partial=True
        )
        db.session.add(user)
        db.session.commit()
        return user_serializer.jsonify(user)
    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "You have missed a required field. Please try again",
        }, HTTPStatus.UNPROCESSABLE_ENTITY


@router.route("/users", methods=["GET"])
@secure_route
def get_all_users():
    try:
        users = UserModel.query.all()
        return user_serializer.jsonify(users, many=True), HTTPStatus.OK
    except SQLAlchemyError:
        return {"message": "There has been an error"}


@router.route("/accuracy/<int:user_id>", methods=["GET"])
@secure_route
def get_accuracy_score(user_id):
    try:
        predictions = PredictionModel.query.all()
        # print(predictions)
        predictions_by_user = []
        for prediction in predictions:
            if prediction.user_id == user_id:
                predictions_by_user.append(prediction)
        accuracy_list = []
        for prediction in predictions_by_user:
            match = db.session.query(MatchModel).get(prediction.match_id)
            if (
                prediction.team_one_score == match.team_one_score
                and prediction.team_two_score == match.team_two_score
            ):
                accuracy_list.append(1)
        print(accuracy_list)
        return {
            "number-of-accurate-games": sum(accuracy_list),
            "games_guessed": len(predictions_by_user),
            "accuracy_score": sum(accuracy_list) / len(predictions_by_user) * 100,
        }

    except SQLAlchemyError:
        return {"message": "There has been an error"}

@router.route("/all_accuracy", methods=["GET"])
@secure_route
def get_all_accuracy():
    try:
        users = UserModel.query.all()
        print(users)
        users = users[1::]
        print(users)
        user_info = []
        for user in users:
            predictions = PredictionModel.query.all()
            # print(predictions)
            predictions_by_user = []
            for prediction in predictions:
                if prediction.user_id == user.id:
                    predictions_by_user.append(prediction)
            accuracy_list = []
            for prediction in predictions_by_user:
                match = db.session.query(MatchModel).get(prediction.match_id)
                if (
                    prediction.team_one_score == match.team_one_score
                    and prediction.team_two_score == match.team_two_score
                ):
                    accuracy_list.append(1)

            print(accuracy_list)
            user_info.append(
                { "user_id" : user.id,
                    "number-of-accurate-games": sum(accuracy_list),
                    "games_guessed": len(predictions_by_user),
                    "accuracy_score": sum(accuracy_list)
                    / len(predictions_by_user)
                    * 100,
                }
            )
        return {"message" : user_info}

    except SQLAlchemyError:
        return {"message": "There has been an error"}
