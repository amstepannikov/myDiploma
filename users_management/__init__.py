from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from users_management.configs import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # регистрация макета страниц
    from users_management.management.routes import management
    from users_management.users.routes import users
    app.register_blueprint(management)
    app.register_blueprint(users)

    # добавляем конфигурацию
    app.config.from_object(Config)

    # добавляем расширения
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app