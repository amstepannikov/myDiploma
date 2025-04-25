from datetime import datetime
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import TimestampSigner
from flask import current_app

from my_blog import db, login_manager


class User(db.Model, UserMixin):
    """
    Таблица пользователей
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # связь с таблицей постов

    def __repr__(self):
        return f"Пользователь('{self.username}, {self.email}', '{self.image_file}')"

    def get_reset_token(self):
        """
        Генерирует токен для сброса пароля
        :return: строка с токеном
        """
        signer = TimestampSigner(current_app.config['SECRET_KEY'])
        return signer.sign(str({'user_id': self.id}))

        # s = TimestampSigner(current_app.config[Config.WTF_CSRF_SECRET_KEY], expires_sec)
        # return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        """
        Проверяет валидность токена для сброса пароля
        :param token: токен, который нужно проверить
        :param max_age: время жизни токена, по умолчанию 30 минут
        :return: id пользователя или None
        """
        signer = TimestampSigner(current_app.config['SECRET_KEY'])

        # signer = token.uysign TimestampSigner(current_app.config[Config.WTF_CSRF_SECRET_KEY])
        # s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # user_id = signer.loads(token)['user_id']
            d = signer.unsign(token, max_age)
            print(d)
        except Exception:
            print(token)
            return None
        # return User.query.get(user_id)
        return None


class Post(db.Model):
    """
    Таблица постов
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка пользователя из базы
    :param user_id: id пользователя
    """
    return User.query.get(int(user_id))
