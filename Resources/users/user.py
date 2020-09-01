"""
User Resource module
"""

import datetime
from uuid import uuid4

import pytz
import redis
from flask import request
from flask_restful import Resource

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
        UserLogin Resource
        Returns:

        """
        user_json = request.get_json()
        user = user_schema.load(user_json,)

        if not is_email_valid(user.email):
            return {"message": get_text("user_email_bad_format").format(
                user.email)}, 400
        if UserModel.find_by_email(user.email):
            return {"message": get_text("user_email_exist")}, 400
        user = user.create_user(user.email, user.password)
        user.save()

        return {"message": get_text("user_registered")}, 201
