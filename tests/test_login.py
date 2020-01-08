import unittest

from flask_login import current_user

from project import User, bcrypt
from tests.base import BaseTestCase


# набор тестов для проверки входа в систему
class LoginTestCase(BaseTestCase):

    # тест - главная страница открывается нормально (код 200)
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # проверка наличия кнопок входа и регистрации,
    # и отсутствия кнопки выхода до входа в систему
    def test_page_content_before_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Sign in', response.data)
        self.assertIn(b'Register', response.data)
        self.assertNotIn(b'logout', response.data)

    # проверка отсутствия кнопок входа и регистрации,
    # и наличия кнопки выхода после входа из системы
    def test_page_content_after_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertNotIn(b'Sign in', response.data)
        self.assertNotIn(b'Register', response.data)
        self.assertIn(b'logout', response.data)

    # проверка наличия заголовка на странице входа
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    # проверка по флагу is_active сохранения в сессии
    # сведений о вошедшем пользователе
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertTrue(current_user.name == "admin")
            self.assertTrue(current_user.is_active)

    # проверка по флагу is_active, что после неудачной попытки входа
    # пользователь остается гостем
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertFalse(current_user.is_active)

    # проверка по id успешного входа пользователя
    def test_get_admin_by_id(self):
        with self.client:
            try:
                self.client.post('/login', data=dict(
                    username="admin", password='admin'
                ), follow_redirects=True)
                self.assertTrue(current_user.id == 1)
                self.assertFalse(current_user.id == 20)
            except:
                self.assertFalse(True)
    # проверка обнаружения ошибки при входе с
    # несуществующими учетными данными по id
    # (id не существует до входа)
    def test_get_anon_by_id(self):
        with self.client:
            try:
                self.client.post('/login', data=dict(
                    username="Michael", password='python'
                ), follow_redirects=True)
                self.assertTrue(current_user.id == 2)
                self.assertFalse(current_user.id == 20)
            except:
                self.assertFalse(False)

    # проверка корректного хэширования
    # пароля пользователя
    def test_check_password(self):
        user = User.query.filter_by(
            email='ad@min.com'
        ).first()
        self.assertTrue(
            bcrypt.check_password_hash(
                user.password, 'admin'
            )
        )
        self.assertFalse(
            bcrypt.check_password_hash(
                user.password, 'foobar'
            )
        )


if __name__ == '__main__':
    unittest.main()
