"""
Authentication tests
"""

from Models.users.user import UserModel as User
from .base_setup import BaseSetup, BASE_URL


class UserAuthenticationTest(BaseSetup):
    payload = {
        'email': 'test@gmail.com',
        'password': 'password1'
    }

    reg_url = BASE_URL + '/auth/register'
    login_url = BASE_URL + '/auth/login'

    def test_create_valid_user_success(self):
        res = self.app.post(self.reg_url, json=self.payload)
        with self.movies_app.app_context():
            user = User.find_by_email(self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertEqual(res.status_code, 201)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails
        """
        new_payload = self.payload
        with self.movies_app.app_context():
            user = User.create_user(**self.payload)
            user.save()
        res = self.app.post(self.reg_url, json=new_payload)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'This email is already registered')

    def test_create_token_for_user(self):
        """
        Test that a access and refresh token are created for a user
        """

        self.app.post(self.reg_url, json=self.payload)
        res = self.app.post(self.login_url, json=self.payload)

        data = res.get_json()
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertEqual(res.status_code, 200)

    def test_create_token_for_user_failed(self):
        """
        Test fail login with wrong credentials
        """

        new_payload = {
            "email": "non@mail.com",
            "password": "pass"
        }
        res = self.app.post(self.login_url, json=new_payload)

        data = res.get_json()
        self.assertIn("email and password incorrect", data['message'])
        self.assertEqual(res.status_code, 401)


