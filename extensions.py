"""
extensions for our application
"""
import os

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS

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
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
marsh = Marshmallow()
cors = CORS()
