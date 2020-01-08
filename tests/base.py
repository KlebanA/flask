from flask_testing import TestCase

from project import app, db
from project.models import User, BlogPost


# базовый класс для наборов тестов -
# содержит методы запуска веб-приложения,
# создания БД в памяти и
# добавления пользователя и поста
class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.add(
            BlogPost("Test post",
            "This is a test. Only a test.",
            "admin"
            )
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
