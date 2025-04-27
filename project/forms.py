from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

from models.model_ex1 import User


class MessageForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])
    message = TextAreaField('Message: ', validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm1(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegistrationForm1(FlaskForm):
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. Пожалуйста, выберите другой')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят Пожалуйста, выберите другой')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом '
                                  'отсутствует. '
                                  'Вы можете зарегистрировать его')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Переустановить пароль')

    # from flask.ext.wtf import Form, RecaptchaField
    # from wtforms import TextField, PasswordField, BooleanField
    # from wtforms.validators import Required, EqualTo, Email
    #
    # class LoginForm(Form):
    #   email = TextField('Email address', [Required(), Email()])
    #   password = PasswordField('Password', [Required()])
    #
    # class RegisterForm(Form):
    #   name = TextField('NickName', [Required()])
    #   email = TextField('Email address', [Required(), Email()])
    #   password = PasswordField('Password', [Required()])
    #   confirm = PasswordField('Repeat Password', [
    #       Required(),
    #       EqualTo('password', message='Passwords must match')
    #       ])
    #   accept_tos = BooleanField('I accept the TOS', [Required()])
    #   recaptcha = RecaptchaField()