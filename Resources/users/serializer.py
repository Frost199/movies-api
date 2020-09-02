"""
User Mode Serializer
"""
from marshmallow import fields

from Models.users.user import UserModel
from extensions import marsh


class UserSchema(marsh.SQLAlchemyAutoSchema):
    """
    User Schema
    """
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    class Meta:
        """
        Meta model for user
        """
        model = UserModel
        load_only = ("password",)
        dump_only = ()
        fields = ('email', 'password',)
        load_instance = True
