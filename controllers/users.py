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
