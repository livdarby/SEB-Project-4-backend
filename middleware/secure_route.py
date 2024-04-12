from functools import wraps
from http import HTTPStatus
from flask import request, g
import jwt
from config.environment import SECRET
from models.user import UserModel
from app import db


def secure_route(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        print("this is the secure route!!!")

        raw_token = request.headers.get("Authorization")
        if not raw_token:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        token = raw_token.replace("Bearer ", "")
        print(token)
        try:
            payload = jwt.decode(token, SECRET, "HS256")
            user_id = payload["sub"]
            user = db.session.query(UserModel).get(user_id)
            g.current_user = user
            print("payload is: ", payload)
            print("current user is: ", g.current_user)
            return route_func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {
                "message": "Token has expired. Please log in again."
            }, HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    return wrapper
