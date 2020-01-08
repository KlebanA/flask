import unittest
from flask_login import current_user
from tests.base import BaseTestCase


# набор тестов для выхода из системы
class LogoutTests(BaseTestCase):

    # тест - после входа и выхода из системы
    # пользователь становится неактивным, гостем
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertFalse(current_user.is_active)

    # тест - при попытке выхода из системы без входа
    # отображается сообщение об ошибке
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


if __name__ == '__main__':
    unittest.main()
