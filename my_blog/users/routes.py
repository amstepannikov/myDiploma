from datetime import datetime, timedelta

from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.google import make_google_blueprint, google

from my_blog import db, bcrypt, google_blueprint
from my_blog.models import User, Post, Role
from my_blog.configs import Config
from my_blog.users.utils import save_picture, send_reset_email
from my_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm)

# Создаем страницу/макета для users
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Регистрация пользователя в системе
    :return: render_template - возвращает шаблон страницы register.html
    """
    # Если пользователь уже залогинен, то мы не можем войти в систему
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Хеширование пароля
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Добавляем пользователя и его роль в базу данных
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        role = Role.query.filter_by(name='member').first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Вход пользователя в систему
    :return: render_template - возвращает шаблон страницы login.html
    """
    # Если пользователь уже залогинен, то мы сразу переходим к постам
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))

    # регистрация через google
    # if not google.authorized:
    #     return f'<a href="{url_for("google.login")}">Sign in with Google</a>'
    # resp = google.get('/oauth2/v2/userinfo')  # Получаем профиль пользователя
    # assert resp.ok, resp.text
    # email = resp.json()['email']
    # print(resp)

    form = LoginForm()

    # Если пользователь уже есть, то мы не можем зарегистрировать пользователя с таким же адресом электронной почты
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Если пользователь существует и пароль верный, то ...
        user_true = user and bcrypt.check_password_hash(user.password, form.password.data)
        if user_true and not user.is_active:
            flash('Аккаунт заблокирован!', 'внимание')
        elif user_true and user.date_change_password + timedelta(days=Config.PASSWORD_TIME) < datetime.now():
            flash('Срок действия пароля истек! Смените пароль, нажав на Сброс пароля', 'внимание')
        elif user_true:
            login_user(user, remember=True)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('posts.all_posts'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)


@users.route('/login_guest')
def login_guest():
    """Авторизация пользователя по умолчанию"""
    user = User.query.filter_by(email='guest@mail.ru').first()
    login_user(user, remember=True)
    return redirect(url_for('posts.all_posts'))


@users.route('/login_google')
def login_google():
    """Авторизация пользователя через Google"""
    user = User.query.filter_by(email='guest@mail.ru').first()
    login_user(user, remember=True)
    return redirect(url_for('posts.all_posts'))


@users.route('/login_github')
def login_github():
    """Авторизация пользователя через Github"""
    user = User.query.filter_by(email='guest@mail.ru').first()
    login_user(user, remember=True)
    return redirect(url_for('posts.all_posts'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Пользователь может обновить информацию о себе
    :return: render_template - возвращает шаблон страницы account.html
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Сохраняем изменения в базе данных
        db.session.commit()
        # Показать сообщение об успешном обновлении аккаунта
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # Показать посты пользователя
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
        avatar = url_for('static', filename='avatars/' + current_user.avatar)
        return render_template('account.html', title='Аккаунт',
                           avatar=avatar, form=form, posts=posts, user=user)
    avatar = url_for('static', filename='avatars/' + current_user.avatar)
    return render_template('account.html', title='Аккаунт', avatar=avatar, form=form)


@users.route("/logout")
def logout():
    """
    Выход из системы
    :return: redirect - возвращает на главную страницу
    """
    # token = google_blueprint.token["access_token"]
    # resp = google.post(
    #     "https://accounts.google.com/o/oauth2/revoke",
    #     params={"token": token},
    #     headers={"Content-Type": "application/x-www-form-urlencoded"}
    # )
    # assert resp.ok, resp.text
    logout_user()
    # del google_blueprint.token
    return redirect(url_for('main.home'))


@users.route("/user/<string:username>")
def user_posts(username):
    """
    Показать посты пользователя
    :param username: имя пользователя
    :return: render_template - возвращает шаблон страницы user_posts.html
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Запрос на сброс пароля
    :return: render_template - возвращает шаблон страницы reset_request.html
    """
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # находим пользователя с указанной почтой
        user = User.query.filter_by(email=form.email.data).first()
        # отправка письма со ссылкой на страницу смены пароля
        send_reset_email(user)
        flash('На почту отправлено письмо с '
              'инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Сброс пароля', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Смена пароля через ссылку из почты
    :param token: токен для смены пароля, получаем из ссылки
    :return: render_template - возвращает шаблон страницы reset_token.html
    """
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))

    # по токену находим пользователя
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        # если пользователя не нашли, отправляем повторно на страницу запроса смены пароля
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! Теперь вы можете авторизоваться', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Сброс пароля', form=form)