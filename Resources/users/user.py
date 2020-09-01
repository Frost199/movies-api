"""
User Resource module
"""

import datetime

import pytz
import redis
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from Models.users.tracking import TrackingModel as TrackLogin
from Models.users.user import UserModel
from Resources.users.serializer import UserSchema
from libs.email import is_email_valid
from libs.strings import get_text

sign_in_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
ACCESS_EXPIRES = datetime.timedelta(hours=1)
ACCESS_LOGIN_EXPIRES = datetime.timedelta(minutes=30)
REFRESH_EXPIRES = datetime.timedelta(days=30)

user_schema = UserSchema()


class UserRegistration(Resource):
    """
    User Login resource for requests
    """

    @classmethod
    def post(cls):
        """
        POST request for registration Resource
        Returns:

        """
        user_json = request.get_json()
        user = user_schema.load(user_json, )

        if not is_email_valid(user.email):
            return {"message": get_text("user_email_bad_format").format(
                user.email)}, 400
        if UserModel.find_by_email(user.email):
            return {"message": get_text("user_email_exist")}, 400
        user = user.create_user(user.email, user.password)
        user.save()

        return {"message": get_text("user_registered")}, 201


class UserLogin(Resource):
    """
    User login resource
    """

    @classmethod
    def post(cls):
        """
        POST requests for login resource
        Returns:

        """
        try:
            user_json = request.get_json()
            user_from_schema = user_schema.load(user_json, )
            user = UserModel.find_by_email(user_from_schema.email)
            user_ip = get_client_ip(request)
            if user and user.check_password(user_from_schema.password):
                if not user.disabled:
                    access_token, refresh_token = generate_auth_token(user,
                                                                      user_ip)
                    time_now = datetime.datetime.now(pytz.utc)
                    user_tracking = TrackLogin(user.id,
                                               ip_address=user_ip,
                                               created_on=time_now)
                    user_tracking.save()
                    return {"access_token": access_token,
                            "refresh_token": refresh_token}, 200
                return {"message": get_text("user_disabled")}, 401
            return {"message": get_text("user_invalid")}, 401

        except Exception as _:
            return {"message": get_text("user_error_logging_in")}, 500


def generate_auth_token(user, location_ip, fresh=True):
    """
    generate auth token
    Returns:

    """
    access_expires = ACCESS_LOGIN_EXPIRES
    refresh_expires = REFRESH_EXPIRES

    access_token = create_access_token(
        identity={"_id": user.id, "email": user.email},
        fresh=fresh,
        expires_delta=access_expires
    )
    refresh_token = create_refresh_token({"_id": user.id,
                                          "email": user.email},
                                         expires_delta=refresh_expires)
    if location_ip != 0:
        user.update_activity_tracking(location_ip)
    return access_token, refresh_token


def get_client_ip(flask_request: request):
    """
    Get a client IP address
    Returns:

    """
    if flask_request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_ip_address = flask_request.environ['REMOTE_ADDR']
    else:
        client_ip_address = flask_request.environ['HTTP_X_FORWARDED_FOR']
    return client_ip_address
