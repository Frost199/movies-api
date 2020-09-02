# """
# Movie Model Serializer
# """
# from marshmallow import fields
#
# from Models.movies.movie import MovieModel
# from extensions import marsh
#
#
# class MovieSchema(marsh.SQLAlchemyAutoSchema):
#     """
#     User Schema
#     """
#     email = fields.Str(required=True)
#     password = fields.Str(required=True)
#
#     class Meta:
#         """
#         Meta model for user
#         """
#         model = MovieModel
#         load_only = ("password",)
#         dump_only = ()
#         fields = ('email', 'password',)
#         load_instance = True
