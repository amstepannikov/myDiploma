import re

from wtforms.validators import ValidationError
from flask_login import current_user

from my_blog.models import User


class RePassword:
    """
    Проверяет наличие символов в обоих регистрах,
    чисел, спецсимволов и минимальную длину символов
    """
    def __init__(self, message=None):
        self.message = message
        self.pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&/*+-])[A-Za-z\d@$!%*#?&/*+-]{4,}$'

    def __call__(self, form, field):
        if field.name != 'password':
            raise ValueError('Данная проверка, только для поля password')

        if (
            field.data
            and isinstance(field.data, str)
            and re.match(self.pattern, field.data)
        ):
            return

        if self.message is None:
            message = field.gettext("Пароль должен содержать символы в обоих регистрах, числа и спецсимволы")
        else:
            message = self.message

        raise ValidationError(message)


class UserNameNotInBase:
    """
    Данное имя пользователя должно отсутствовать в базе
    """

    def __init__(self, message=None, current=False):
        self.message = message
        self.current = current

    def __call__(self, form, field):
        if field.name != 'username':
            raise ValueError('Данная проверка, только для поля username')

        if self.current and current_user.username == field.data:
            return

        if (
            field.data
            and isinstance(field.data, str)
            and not User.query.filter_by(username=field.data).first()
        ):
            return

        if self.message is None:
            message = field.gettext("Это имя занято. Пожалуйста, выберите другое.")
        else:
            message = self.message

        raise ValidationError(message)


class EmailNotInBase:
    """
    Данный email должно отсутствовать в базе
    """

    def __init__(self, message=None, current=False):
        self.message = message
        self.current = current

    def __call__(self, form, field):
        if field.name != 'email':
            raise ValueError('Данная проверка, только для поля email')

        if self.current and current_user.email == field.data:
            return

        if (
            field.data
            and isinstance(field.data, str)
            and not User.query.filter_by(email=field.data).first()
        ):
            return

        if self.message is None:
            message = field.gettext("Этот email занят Пожалуйста, выберите другой.")
        else:
            message = self.message

        raise ValidationError(message)


class EmailInBase:
    """
    Данный email должно присутствовать в базе
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.name != 'email':
            raise ValueError('Данная проверка, только для поля email')

        if (
            field.data
            and isinstance(field.data, str)
            and User.query.filter_by(email=field.data).first()
        ):
            return

        if self.message is None:
            message = field.gettext("Аккаунт с данным email-адресом отсутствует.")
        else:
            message = self.message

        raise ValidationError(message)