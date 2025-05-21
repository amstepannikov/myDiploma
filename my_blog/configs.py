import os

# переменная, в которую помещается исполняемая директория скрипта;
# basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Класс, который используется для создания базового конфига.

    DEBUG определяет появление сообщений об ошибках в тестовом окружении;
    ADMINS содержит адрес электронной почты администраторов для рассылок из приложения;
    DATABASE_CONNECT_OPTIONS, как несложно догадаться — опции подключения SQLAlchemy;
    THREADS_PER_PAGE, как мне кажется, ставил 2 на ядро… Могу ошибаться;
    WTF_CSRF_ENABLED и WTF_CSRF_SECRET_KEY защищают от подмены POST-сообщений;
    RECAPTCHA_* используется для входящего в WTForms поля RecaptchaField. Получить приватный и публичный ключи можно на сайте **recaptcha
    """
    # переменная, в которую помещается исполняемая директория скрипта;
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    ADMINS = frozenset(['youremail@yourdomain.com'])

    # Используется для подписи cookies, при его изменении пользователям потребуется логиниться заново
    SECRET_KEY = 'c018c942bbf625466a3ea0369918eac1f254fecc48452f56da2f1cf839c9e749'

    # Путь к файлу базы данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/app.db')

    DATABASE_CONNECT_OPTIONS = {}

    GOOGLE_OAUTH_CLIENT_ID = '' # убрать при Push в GitHub
    GOOGLE_OAUTH_CLIENT_SECRET = '' # убрать при Push в GitHub

    # Почта, используемая для рассылки сообщений
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'krivko_kod@mail.ru'
    MAIL_PASSWORD = 'XpGPCXxc92Y4kidVa2ib'
    DEFAULT_MAIL_SENDER = 'krivko_kod@mail.ru'
    MAIL_SUPPRESS_SEND = False # Если True, то это тестовая рассылка и письма не отправляются

    THREADS_PER_PAGE = 8

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    # Сколько дней действует пароль пользователя
    PASSWORD_TIME = 30


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True