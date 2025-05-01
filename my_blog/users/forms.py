from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from my_blog.users.validators import UserNameNotInBase, EmailNotInBase
from my_blog.models import User


class RegistrationForm(FlaskForm):
    """
    Форма для регистрации пользователя.
    """
    username = StringField('Имя пользователя:', validators=[DataRequired(), Length(min=2, max=20), UserNameNotInBase()])
    email = StringField('Email:', validators=[DataRequired(), Email(message='Неправильное имя почты'), EmailNotInBase()])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователя.
    """
    email = StringField('Email:', validators=[DataRequired(), Email(message='Неправильное имя почты')])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    """
    Форма для обновления профиля пользователя.
    """
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20), UserNameNotInBase(current=True)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неправильное имя почты'), EmailNotInBase(current=True)])
    picture = FileField('Обновить аватарку профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')


class RequestResetForm(FlaskForm):
    """
    Форма для отправки запроса восстановления пароля, через почту
    """
    @staticmethod
    def in_email(form, field):
        """Проверка на наличие email в базе"""
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом отсутствует. Вы можете зарегистрировать его')

    email = StringField('Укажите Email вашего аккаунта', validators=[DataRequired(), Email(message='Неправильное имя почты'), in_email])
    submit = SubmitField('Отправить письмо для изменения пароля')


class ResetPasswordForm(FlaskForm):
    """
    Форма для восстановления пароля.
    """
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Переустановить пароль')