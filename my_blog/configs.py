import os


class Config:
    """Класс, который используется для создания базового конфига"""

    # переменная, в которую помещается исполняемая директория скрипта;
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Используется для подписи cookies, при его изменении пользователям потребуется логиниться заново
    SECRET_KEY = 'c018c942bbf625466a3ea0369918eac1f254fecc48452f56da2f1cf839c9e749'

    # Путь к файлу базы данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/app.db')

    # Переменные, используемые для авторизации через Google
    GOOGLE_OAUTH_CLIENT_ID = '' # убрать при Push в GitHub
    GOOGLE_OAUTH_CLIENT_SECRET = '' # убрать при Push в GitHub

    # Переменные, используемые для авторизации через GitHub
    GITHUB_OAUTH_CLIENT_ID = '' # убрать при Push в GitHub
    GITHUB_OAUTH_CLIENT_SECRET = '' # убрать при Push в GitHub

    # Почта, используемая для рассылки сообщений
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'krivko_kod@mail.ru'
    MAIL_PASSWORD = 'XpGPCXxc92Y4kidVa2ib'
    DEFAULT_MAIL_SENDER = 'krivko_kod@mail.ru'
    MAIL_SUPPRESS_SEND = False # Если True, то это тестовая рассылка и письма не отправляются

    # Сколько дней действует пароль пользователя
    PASSWORD_TIME = 30