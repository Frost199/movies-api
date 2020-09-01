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
        self.payload['email'] = 'new@mail.com'
        with self.movies_app.app_context():
            user = User.create_user(**self.payload)
            user.save()
        res = self.app.post(self.reg_url, json=self.payload)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'This email is already registered')
