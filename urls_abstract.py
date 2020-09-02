"""
Urls Interface
"""

import abc
from flask import Flask
from flask_restful import Api


class AbsUrls(metaclass=abc.ABCMeta):
    """
    Urls Interface
    """
    def __init__(self):
        self.app = None

    @staticmethod
    def register_application(application: Flask) -> Api:
        """
        register a python application with flask restful
        Args:
            application:

        Returns:

        """
        return Api(application, prefix='/api/v1')

    @staticmethod
    @abc.abstractmethod
    def add_url(api: Api):
        """
        add urls
        Args:
            api: Flask restful Api
        Returns:
        """
