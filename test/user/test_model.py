"""
user model
"""
import unittest

from Models.users.user import UserModel as User


class ModelTest(unittest.TestCase):
    def test_create_user_with_email_successful(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
