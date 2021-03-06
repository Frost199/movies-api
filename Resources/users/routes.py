"""
User Resource Url module
"""
from flask_restful import Api

from urls_abstract import AbsUrls
from Resources.users.user import UserRegistration, UserLogin, TokenRefresh


class UserUrl(AbsUrls):
    """
    Register User Urls
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def add_url(api: Api):
        """
        Concrete Implementation of adding url
        Args:
            api: Flask restful APi
        Returns:

        """
        api.add_resource(UserRegistration, '/auth/register')
        api.add_resource(UserLogin, '/auth/login')
        api.add_resource(TokenRefresh, '/auth/refresh-token')
