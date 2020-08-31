"""
Flask base app for Movies API
"""
from flask import Flask
from dotenv import load_dotenv
from celery import Celery
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv(".env", verbose=True)

CELERY_TASK_LIST = []


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        """
        A task context for celery
        """
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Creating a Flask application using the app factory pattern
    Args:
        settings_override: Override settings
    Returns: Flask app

    """

    application = Flask(__name__, instance_relative_config=True)

    application.config.from_object("instance.settings")
    application.config.from_pyfile("settings.py", silent=True)

    if settings_override:
        application.config.update(settings_override)

    application.logger.setLevel(application.config["LOG_LEVEL"])
    middleware(application)

    return application


def middleware(application):
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
celery__init = create_celery_app()

if __name__ == "__main__":
    movies_app.run()
