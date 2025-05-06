import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
from itsdangerous import URLSafeTimedSerializer

from my_blog.configs import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate()

# Создаем объект сериализатора с секретным ключом
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

# создаем макет для регистрации в google
google_blueprint = make_google_blueprint(
    client_id=Config.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=Config.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=['profile', 'email']
)


def create_app():
    app = Flask(__name__)

    # добавляем конфигурацию, после чего к ней нужно обращаться через current_app.config['KEY']
    app.config.from_object(Config)

    # регистрация макета страниц
    from my_blog.main.routes import main
    from my_blog.users.routes import users
    from my_blog.posts.routes import posts
    from my_blog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(google_blueprint, url_prefix='/login')
    app.register_blueprint(errors)

    # добавляем расширения
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    return app