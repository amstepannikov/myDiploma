from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from my_blog.configs import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # регистрация макета страниц
    from my_blog.main.routes import main
    from my_blog.users.routes import users
    from my_blog.posts.routes import posts
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    # добавляем конфигурацию, после чего к ней нужно обращаться через current_app.config['KEY']
    app.config.from_object(Config)

    # добавляем расширения
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    return app