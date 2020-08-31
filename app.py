"""
Flask base app for Movies API
"""
from flask import Flask
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv(".env", verbose=True)


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


movies_app = create_app()

if __name__ == "__main__":
    movies_app.run()
