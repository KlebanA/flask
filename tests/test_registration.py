import unittest

from flask_login import current_user
from flask import request

from tests.base import BaseTestCase
from project.models import User


class RegistrationTests(BaseTestCase):
    # проверка регистрации пользователя и
    # входа в систему сразу при регистрации
    def test_user_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='Michael', email='michael@realpython.com',
                password='python', confirm='python'
            ), follow_redirects=True)

            self.assertNotIn(b'Sign in', response.data)
            self.assertNotIn(b'Register', response.data)
            self.assertIn(b'logout', response.data)

            self.assertTrue(current_user.name == "Michael")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(
                email='michael@realpython.com'
            ).first()
            self.assertTrue(
                str(user) == '<name - Michael, anon - False>'
            )

    # проверка обнаружения неправильного e-mail при регистрации
    def test_wrong_email_user_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='Michael', email='michael',
                password='python', confirm='python'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn('/register', request.url)

    # проверка обнаружения попытки регистрации
    # пользователя с существующим логином
    def test_existing_login_user_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='admin', email='ad@min.com',
                password='admin', confirm='admin'
            ), follow_redirects=True)
            self.assertIn('/register', request.url)


if __name__ == '__main__':
    unittest.main()
