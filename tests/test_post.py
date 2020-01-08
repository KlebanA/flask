import unittest
from tests.base import BaseTestCase


# набор тестов для отправки сообщений
class BlogPostTests(BaseTestCase):
    # проверка возможности отправки
    # постов пользователем
    def test_user_can_post(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.post(
                '/',
                data=dict(title="test", description="test"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

    # проверка, что гость не может отправлять посты
    def test_anon_can_post(self):
        with self.client:
            response = self.client.post(
                '/',
                data=dict(title="test", description="test"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
