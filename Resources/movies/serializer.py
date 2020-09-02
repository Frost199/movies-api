"""
Movie Model Serializer
"""
from marshmallow import fields
from marshmallow.validate import Range

from Models.movies.movie import MovieModel
from extensions import marsh


class MovieSchema(marsh.SQLAlchemyAutoSchema):
    """
    User Schema
    """
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    rating = fields.Float(required=True, validate=Range(min=1, max=5,
                                                        max_inclusive=True))

    class Meta:
        """
        Meta model for user
        """
        model = MovieModel
        fields = ('title', 'description', 'rating',)
        load_instance = True


class UpdateMovieSchema(marsh.SQLAlchemyAutoSchema):
    """
    User Schema
    """
    title = fields.Str(required=True)
    rating = fields.Float(required=True, validate=Range(min=1, max=5,
                                                        max_inclusive=True))

    class Meta:
        """
        Meta model for user
        """
        model = MovieModel
        fields = ('title', 'rating',)
        load_instance = True


class DeleteMovieSchema(marsh.SQLAlchemyAutoSchema):
    """
    User Schema
    """
    title = fields.Str(required=True)

    class Meta:
        """
        Meta model for user
        """
        model = MovieModel
        fields = ('title',)
        load_instance = True
