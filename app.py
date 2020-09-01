"""
Flask base app for Movies API
"""
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
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
jwt = JWTManager(movies_app)


# adding claims to a jwt to check somethings the user claims to be
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """
    Add claims to a JWT identity
    Args:
        identity: User identity
    Returns:
        JSON of type Boolean
    """
    from Models.users.user import UserModel
    admin = UserModel.query.first()

    # instead of hard coding, read from database or config file
    if identity["_id"] == admin.id:
        return {"is_admin": True}
    return {"is_admin": False}


# customised message for expired JWT token
@jwt.expired_token_loader
def expired_token_callback():
    """
    Custom Error message for an expired token
    Returns:
        JSON and Status code
    """
    return (
        jsonify({"description": "This token has expired",
                 "error": "token_expired"}),
        401,
    )


# customised message for an invalid token
@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Customized message for a token that is invalid
    Args:
        error: error passed
    Returns:
        JSON and Status code
    """
    return (
        jsonify(
            {"description": "Signature verification failed",
             "error": "invalid_token"}
        ),
        401,
    )


# customised message when no Jwt is present
@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Missing token customized message
    Args:
        error: Error passed

    Returns:
        JSON and Status code
    """
    return (
        jsonify(
            {
                "description": "Request doe not contain an access token",
                "error": "authorization_required",
            }
        ),
        401,
    )


# customised message for a fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """
    When a token is not fresh
    Returns:
        JSON and Status code
    """
    return (
        jsonify({"description": "Token is not fresh",
                 "error": "fresh_token_required"}),
        401,
    )


# Revoking a token when user logs out or token has being revoked
@jwt.revoked_token_loader
def revoked_token_loader():
    """
    Message when a token is revoked
    Returns:

    """
    return (
        jsonify(
            {"description": "The token has been revoked",
             "error": "token_revoked"}
        ),
        401,
    )


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
