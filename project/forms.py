from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class MessageForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])
    message = TextAreaField('Message: ', validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])


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