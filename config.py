

# базовая конфигурация, которую наследуют все остальные
class BaseConfig(object):
    SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8b\x0c...'


# отладочная конфигурация, используемая при запуске приложения,
# с адресом БД в файловой системе
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sample.db'


# рабочая конфигурация, используемая при запуске приложения,
# с адресом БД в файловой системе
class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sample.db'
# тестовая конфигурация, используемая при запуске тестов,
# с адресом БД в памяти
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
# тестовая конфигурация, используемая при запуске тестов,
# с адресом БД в памяти
class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
