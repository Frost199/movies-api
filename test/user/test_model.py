"""
user model
"""
import unittest

from Models.users.user import UserModel as User


class ModelTest(unittest.TestCase):
    def test_create_user_with_email_successful(self):
        """
        Test creating a user is successful
        Returns:

        """
        email = 'don.joe@example.com'
        password = 'password'
        user = User()
        user = user.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized

        Returns:

        """
        email = 'don.joe@EXAMPLE.COM'
        user = User()
        user = user.create_user(email, 'qwerty  uiop12')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating new user with no email raises error
        Returns:
        """
        with self.assertRaises(ValueError):
            User.create_user("", "testPass")
        with self.assertRaises(ValueError):
            User.create_user(None, "testPass")

    def test_create_new_superuser(self):
        """
        Test creating a new super user
        Returns:

        """
        user = User.create_superuser(
            'jane.joe@example.com',
            'test123'
        )
        self.assertEqual('Admin', user.role)


if __name__ == '__main__':
    unittest.main()
