from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

from my_blog.models import User


class RegistrationForm(FlaskForm):
    """
    Форма для регистрации пользователя.
    """
    username = StringField('Имя пользователя:', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        """
        Проверяет, не занято ли имя пользователя.
        :param username: Имя пользователя, которое необходимо проверить на уникальность.
        :return: None
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        """
        Проверяет, не занят ли email пользователя.
        :param email: Email пользователя, который необходимо проверить на уникальность.
        :return: None
        """
        print(email)
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователя.
    """
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    """
    Форма для обновления профиля пользователя.
    """
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        """
        Проверяет, не занято ли имя пользователя.
        :param username: Имя пользователя, которое необходимо проверить на уникальность.
        :return: None
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. Пожалуйста, выберите другой')

    def validate_email(self, email):
        """
        Проверяет, не занят ли email пользователя.
        :param email: Email пользователя, который необходимо проверить на уникальность.
        :return: None
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят Пожалуйста, выберите другой')


class RequestResetForm(FlaskForm):
    """
    Форма для запроса восстановления пароля.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом отсутствует. Вы можете зарегистрировать его')


class ResetPasswordForm(FlaskForm):
    """
    Форма для восстановления пароля.
    """
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Переустановить пароль')