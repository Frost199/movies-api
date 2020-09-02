"""
Flask Config, this config should
"""
import os

DEBUG = True
SECRET_KEY = os.environ["APP_SECRET_KEY"]
LOG_LEVEL = "DEBUG"

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                         "sqlite:///database/movies.db"
                                         )
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
