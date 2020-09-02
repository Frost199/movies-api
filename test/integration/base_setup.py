"""
Base setup for integration tests
"""
import os
import unittest


from app import movies_app
from extensions import db

TEST_DB = 'test_movies.db'
BASE_URL = 'http://127.0.0.1:5000/api/v1'


class BaseSetup(unittest.TestCase):

    def setUp(self) -> None:
        """
        BAse setup
        Returns:

        """
        self.movies_app = movies_app
        self.movies_app.config['TESTING'] = True
        self.movies_app.config['DEBUG'] = False
        self.movies_app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///test/integration/' + TEST_DB
        db.init_app(movies_app)
        with self.movies_app.app_context():
            self.app = self.movies_app.test_client()
            db.drop_all()
            db.create_all()

    def tearDown(self) -> None:
        """
        clean up after the test
        Returns:

        """
        db_path = os.getcwd() + '/test/integration/test_movies.db'
        os.remove(db_path)
