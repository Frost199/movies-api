"""
Flask base app for Movies API
"""
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from marshmallow import ValidationError

from Resources.users.routes import UserUrl
from urls_abstract import AbsUrls

load_dotenv(".env", verbose=True)

from extensions import db, marsh, cors


def create_app(settings_override=None) -> Flask:
    """
    Creating a Flask application using the app factory pattern
    Args:
        settings_override: Override settings
    Returns: Flask app

    """

    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object("config.settings")
    application.config.from_pyfile("settings.py", silent=True)

    if settings_override:
        application.config.update(settings_override)

    application.logger.setLevel(application.config["LOG_LEVEL"])
    middleware(application)
    extension(application)
    register_resource(application)
    db_migrate(application, db)

    return application


def middleware(application: Flask) -> None:
    """
    Register 0 or more middleware (mutates the app passed in).

    :param application: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even
    # if behind a proxy.
    application.wsgi_app = ProxyFix(application.wsgi_app)

    return None


def register_resource(application: Flask):
    """
    Register API resource
    :param application:
    :return:
    """
    api = AbsUrls.register_application(application)
    UserUrl.add_url(api)


def db_migrate(application: Flask, db_to_migrate: db) -> None:
    """
    Handling database migration
    :param application:
    :param db_to_migrate:
    :return:
    """
    Migrate(application, db_to_migrate)


def extension(application: Flask) -> None:
    """
    Register 0 or more extensions (mutates the app passed in)
    Args:
        application: Flask application instance

    Returns: None

    """
    db.init_app(application)
    marsh.init_app(application)
    cors.init_app(application)


movies_app = create_app()


@movies_app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    """
    Handle Marshmallow serialization errors
    :param err:
    :return:
    """
    return jsonify(err.messages), 400


if __name__ == "__main__":
    movies_app.run()
