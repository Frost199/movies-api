"""
Movie Resource for user
"""
from typing import Dict

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from Services.movie_service import get_movies
from libs.strings import get_text

MOVIES_URL = 'https://api.themoviedb.org/3/movie/popular?api_key='
MOVIES_PER_PAGE = 20
MOVIES_MAX_PAGINATION = 10
MOVIES_MIN_PAGINATION = 1


class MoviesList(Resource):
    """
    Movies list resource class
    """

    @classmethod
    @jwt_required
    def get(cls, page: int):
        """
        get movies from an external API
        Returns:
        """
        if page < MOVIES_MIN_PAGINATION or page > MOVIES_MAX_PAGINATION:
            return ({"message": get_text(
                "movies_pagination_out_bounds").format(
                MOVIES_MIN_PAGINATION, MOVIES_MAX_PAGINATION)},
                    400)
        response = get_movies(
            MOVIES_URL + '849f15719681915156404e9a0cd9a744&language=en-US',
            page)
        response = response.json()
        result = response['results']
        result = result[:20]
        return {"movies": result}, 200
