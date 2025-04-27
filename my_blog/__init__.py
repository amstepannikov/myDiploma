import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_dance.contrib.google import make_google_blueprint, google

from my_blog.configs import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

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
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(google_blueprint, url_prefix='/login')

    # добавляем расширения
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    return app