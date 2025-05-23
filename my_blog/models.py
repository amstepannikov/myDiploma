from datetime import datetime

from flask_login import UserMixin

from my_blog import db, login_manager, serializer


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
        # Данные для сериализации
        data_to_serialize = {'user_id': self.id}
        # Сериализация данных
        token = serializer.dumps(data_to_serialize, salt="email-confirm")
        return token

    @staticmethod
    def verify_reset_token(token, max_age=18000):
        """
        Проверяет валидность токена для сброса пароля в ссылке из почты
        :param token: токен, который нужно проверить
        :param max_age: время жизни токена, по умолчанию 30 минут
        :return: объект User или None (в случае ошибки)
        """
        try:
            decoded_data = serializer.loads(token, max_age=max_age, salt="email-confirm")
            user_id = decoded_data['user_id']
            user = User.query.get(user_id)
        except Exception as e:
             return None
        return user


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
