"""
Movie Model
"""
from extensions import db
from libs.sqlalchemy_util import AwareDateTime
from libs.util_datetime import tzware_datetime


class MovieModel(db.Model):
    """
    A class for making a movie model
    """
    __tablename__ = "movie"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    created_on = db.Column(AwareDateTime(), default=tzware_datetime,
                           nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("UserModel")
