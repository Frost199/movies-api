"""
Movie Resource for user
"""
import os

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from Models import MovieModel
from Resources.movies.serializer import MovieSchema, UpdateMovieSchema, \
    DeleteMovieSchema
from Services.movie_service import get_movies
from libs.strings import get_text

MOVIES_URL = 'https://api.themoviedb.org/3/movie/popular?api_key=' + \
             os.environ.get("MOVIE_API_KEY")
MOVIES_PER_PAGE = 20
MOVIES_MAX_PAGINATION = 10
MOVIES_MIN_PAGINATION = 1

movie_schema = MovieSchema()
update_movie_schema = UpdateMovieSchema()
delete_movie_schema = DeleteMovieSchema()


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
            MOVIES_URL + '&language=en-US',
            page)
        response = response.json()
        result = response['results']
        result = result[:20]
        return {"movies": result}, 200


class Movies(Resource):
    """
    User personalised Movie resource
    """

    @classmethod
    def load_movie_and_user(cls, schema):
        """
        get a movie
        Args:
            schema: schema to lad for a movie
        Returns:

        """
        current_user = get_jwt_identity()
        movie_json = request.get_json()
        movie = schema.load(movie_json, )
        user_id = current_user["_id"]
        title = movie_json['title']
        return current_user, movie, user_id, title

    @classmethod
    @jwt_required
    def post(cls):
        """
        POST request to add a movie
        Returns:

        """

        current_user, movie, user_id, title = cls.load_movie_and_user(
            movie_schema)

        try:
            movie_available = movie.find_by_title_and_user_id(title, user_id)
            if not movie_available:
                title = movie.title
                description = movie.description
                rating = movie.rating
                movie = MovieModel()
                movie.create_movie(title, description, rating, current_user[
                    "_id"])
                movie.save()
                return {"message": get_text("movie_created"),
                        "movie": movie.json}, 201
            return {"message": get_text("movie_exist").format(title)}, 400
        except Exception as _:
            print(_)
            return {"message": get_text("error_adding_movie")}, 500

    @classmethod
    @jwt_required
    def put(cls):
        """
        Update a movie rating
        Returns:

        """
        current_user, movie, user_id, title = cls.load_movie_and_user(
            update_movie_schema)
        try:
            movie_available = movie.find_by_title_and_user_id(title, user_id)
            if not movie_available:
                return {"message": get_text("movie_not_exist").format(
                    title)}, \
                       404
            movie_available.update_movie_rating(movie.rating)
            movie_available.save()
            return {"message": get_text("movie_updated").format(title),
                    "movie": movie_available.json}, 200

        except Exception as _:
            return {"message": get_text("error_updating_movie")}, 500

    @classmethod
    @jwt_required
    def delete(cls):
        """
        Remove a movie from a list
        Returns:
        """
        current_user, movie, user_id, title = cls.load_movie_and_user(
            delete_movie_schema)
        try:
            movie_available = movie.find_by_title_and_user_id(title, user_id)
            if not movie_available:
                return {"message": get_text("movie_not_exist").format(
                    title)}, 404
            movie_available.remove()
            return {"message": get_text("movie_removed").format(
                title)}, 200
        except Exception as _:
            return {"message": get_text("error_deleting_movie")}, 500
