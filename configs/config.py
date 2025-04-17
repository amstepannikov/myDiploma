import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    _basedir — переменная, в которую помещается исполняемая директория скрипта;
    DEBUG определяет появление сообщений об ошибках в тестовом окружении;
    SECRET_KEY используется для подписи cookies, при его изменении пользователям потребуется логиниться заново;
    ADMINS содержит адрес электронной почты администраторов для рассылок из приложения;
    SQLALCHEMY_DATABASE_URI и DATABASE_CONNECT_OPTIONS, как несложно догадаться — опции подключения SQLAlchemy;
    THREADS_PER_PAGE, как мне кажется, ставил 2 на ядро… Могу ошибаться;
    WTF_CSRF_ENABLED и WTF_CSRF_SECRET_KEY защищают от подмены POST-сообщений;
    RECAPTCHA_* используется для входящего в WTForms поля RecaptchaField. Получить приватный и публичный ключи можно на сайте **recaptcha
    """
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    ADMINS = frozenset(['youremail@yourdomain.com'])
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'any_key'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DATABASE_CONNECT_OPTIONS = {}

    THREADS_PER_PAGE = 8

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True