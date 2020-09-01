"""
extensions for our application
"""
import uuid

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS


def auto_constraint_name(constraint, table):
    """
    create an auto constraint name which helps cover the bug in sqlite
    Args:
        constraint:
        table:

    Returns:

    """
    if constraint.name is None or constraint.name == "_unnamed_":
        return "sa_autoname_%s" % str(uuid.uuid4())[0:5]
    else:
        return constraint.name


"""
for the convention:
* ix means index names, whenever we create a new index in sqlalchemy, 
  we give it a name
* uq means unique constraints
* ck means check constraint
* fk means foreign key constraint
* pk means primary key constraint
"""
convention = {
    "auto_constraint_name": auto_constraint_name,
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(auto_constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
marsh = Marshmallow()
cors = CORS()
