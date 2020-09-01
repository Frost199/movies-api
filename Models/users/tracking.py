"""
models.users.tracking a user tracking class
"""
from extensions import db
from libs.sqlalchemy_util import AwareDateTime
from libs.util_datetime import tzware_datetime


class TrackingModel(db.Model):
    """
    User tracking model
    """
    __tablename__ = 'tracking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(45))
    created_on = db.Column(AwareDateTime(), default=tzware_datetime,
                           nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super(TrackingModel, self).__init__(**kwargs)
        self.user_id = user_id
        self.ip_address = kwargs['ip_address']
        self.created_on = kwargs['created_on']

    def save(self) -> None:
        """
        save tracking to db
        Returns:

        """
        db.session.add(self)
        db.session.commit()
