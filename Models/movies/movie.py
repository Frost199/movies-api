"""
Movie Model
"""
import datetime
from uuid import uuid4

import pytz

from extensions import db
from libs.sqlalchemy_util import AwareDateTime
from libs.util_datetime import tzware_datetime


class MovieModel(db.Model):
    """
    A class for making a movie model
    """
    __tablename__ = "movie"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    created_on = db.Column(AwareDateTime(), default=tzware_datetime,
                           nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("UserModel")

    @property
    def json(self):
        """
        Dictionary object for user
        Returns:

        """
        return {
            "movie_id": self.id,
            "title": self.title,
            "description": self.description,
            "rating": self.rating,
        }

    def create_movie(self, title: str, description: str, rating: float,
                     user_id: str) -> "MovieModel":
        """
        create a movie and return a Movie object
        Args:
            title: Movie title
            description: movie description
            rating: movie rating
            user_id: user id creating the movie
        Returns:

        """
        self.title = title
        self.description = description
        self.rating = rating
        self.id = uuid4().hex
        self.created_on = datetime.datetime.now(pytz.utc)
        self.user_id = user_id

        return self

    def update_movie_rating(self, rating: float) -> "MovieModel":
        """
        update a movie rating and return a Movie object
        Args:
            rating: user id creating the movie
        Returns:

        """
        self.rating = rating

        return self

    @classmethod
    def find_by_title(cls, title: str) -> "MovieModel":
        """
        Find a movie by title
        Args:
            title: title value to use in searching for movie

        Returns:
            UserModel class object
        """
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_title_and_user_id(cls, title: str, user_id: str) -> \
            "MovieModel":
        """
        Find a movie by title and user_id
        Args:
            title: title value to use in searching for movie
            user_id: user_id value to use in searching for movie
        Returns:
            UserModel class object
        """
        return cls.query.filter_by(title=title, user_id=user_id).first()

    def save(self) -> None:
        """
        Save movie to db
        Returns:

        """
        db.session.add(self)
        db.session.commit()

    def remove(self) -> None:
        """
        Remove movie from db
        Returns:

        """
        db.session.delete(self)
        db.session.commit()
