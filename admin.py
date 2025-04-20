from flask import Flask, render_template, request, redirect, url_for


from project.forms import MessageForm, RegistrationForm
from configs.config import Config


app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app) # инициализируем объект БД


# from flask.ext.login import LoginManager, current_user
# # Инициализируем его и задаем действие "входа"
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# # Задаем обработчик, возвращающий пользователя по Id, либо None. Здесь пользователь запрашивается из базы.
# @login_manager.user_loader
# def load_user(userid):
#     from models import User
#     return User.query.get(int(userid))
#
# # Задаем обработчик before_request, в котором добавляем к глобально-локальному контексту текущего пользователя
# @app.before_request
# def before_request():
#     g.user = current_user

menu = [1, 2, 3]

@app.route('/')
def index():
    return render_template('html/index.html')


@app.route('/about')
def about():
    return render_template('html/about.html', title='О программе', menu=menu)


@app.route('/message/', methods=['get', 'post'])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(name)
        print(email)
        print("\nData received. Now redirecting...")
        return redirect(url_for('message'))

    return render_template('html/message.html', form=form)


@app.route('/registration/', methods=['get', 'post'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        password_repeat = form.password_repeat.data
        print(name)
        print(email)
        print(password)
        print(password_repeat)
        print("\nData received. Now redirecting...")
        return redirect(url_for('message'))

    return render_template('html/message.html', form=form, title='Регистрация')

@app.route('/login')
def login():
    return render_template('html/login.html')


@app.route('/admin/')
def admin():
    if not loggedin:
        return redirect(url_for('login')) # если не залогинен, выполнять редирект на страницу входа
    return render_template('html/admin.html', title='Админка')


if __name__ == "__main__":
    loggedin = True
    app.run(host="localhost", port=5000, debug=True)