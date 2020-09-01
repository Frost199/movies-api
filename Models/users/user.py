"""
User Model
"""
import datetime
from collections import OrderedDict
from uuid import uuid4

import pytz
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from libs.email import normalize_email
from libs.sqlalchemy_util import AwareDateTime
from libs.util_datetime import tzware_datetime


class UserModel(db.Model):
    """
    A user Model class
    """

    __tablename__ = "user"

    ROLE = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin'),
    ])

    id = db.Column(db.String, primary_key=True)
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False),
                     index=True, nullable=False, server_default='member')
    disabled = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(80), nullable=True, unique=True)

    created_on = db.Column(AwareDateTime(), default=tzware_datetime,
                           nullable=False)
    updated_on = db.Column(AwareDateTime(),
                           default=tzware_datetime,
                           onupdate=tzware_datetime)

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    @staticmethod
    def create_user(email: str, password: str) -> "UserModel":
        """
        create a user and return a user
        Returns:

        """
        user = UserModel()
        if email is None or email == "":
            raise ValueError("email must be provided")
        user.email = normalize_email(email)
        user.password = UserModel.encrypt_password(password)
        user.id = uuid4().hex
        user.created_on = datetime.datetime.now(pytz.utc)

        return user

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        """
        find user by email
        :param email:
        :return:
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        """
        find user by id
        :param _id:
        :return:
        """
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def create_superuser(email: str, password: str) -> "UserModel":
        """
        create a user and return a user
        Returns:

        """
        user = UserModel()
        if email is None or email == "":
            raise ValueError("email must be provided")
        user.email = normalize_email(email)
        user.password = UserModel.encrypt_password(password)
        user.role = 'Admin'

        return user

    def check_password(self, password: str) -> bool:
        """
        Ensure a user is authenticated, checking their password.
        Args:
            password: plain password to be checked with

        Returns:
           bool
        """
        return check_password_hash(self.password, password)

    @staticmethod
    def encrypt_password(password: str) -> str:
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.
        Args:
            password: plain password to be checked with

        Returns:
            str
        """
        return generate_password_hash(password)

    def save(self) -> None:
        """
        save user to db
        Returns:

        """
        db.session.add(self)
        db.session.commit()
