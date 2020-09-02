"""
User Resource Url module
"""
from flask_restful import Api

from Resources.movies.movies import MoviesList
from urls_abstract import AbsUrls


class MoviesUrl(AbsUrls):
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
        api.add_resource(MoviesList, "/movies/external/<int:page>")
