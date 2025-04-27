from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import smtplib
import dns.resolver

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24).hex()

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


def verify_email(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = mx_records[0].exchange.to_text()
        with smtplib.SMTP(mx_host, timeout=10) as server:
            server.set_debuglevel(0)
            server.helo()
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            print(f"SMTP response for {email}: code={code}, message={message}")  # Отладочный вывод
            return code == 250
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, smtplib.SMTPException) as e:
        print(f"Error verifying email {email}: {e}")  # Отладочный вывод
        return False


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    try:
        users = User.query.with_entities(User.id, User.username).all()
        return render_template('html/home.html', users=users)
    except Exception as e:
        flash(f'Ошибка базы данных: {str(e)}')
        return render_template('html/home.html', users=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Валидация полей
        if not all([username, email, password, confirm_password]):
            flash('Все поля должны быть заполнены!')
            return redirect(url_for('register'))

        # Проверка совпадения паролей
        if password != confirm_password:
            flash('Пароли не совпадают!')
            return redirect(url_for('register'))

        # Проверка формата email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash('Неверный формат электронной почты!')
            return redirect(url_for('register'))

        # Проверка уникальности имени пользователя
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует!')
            return redirect(url_for('register'))

        # Проверка уникальности email
        if User.query.filter_by(email=email).first():
            flash('Пользователь с такой почтой уже существует!')
            return redirect(url_for('register'))

        # Проверка существования email через SMTP
        if not verify_email(email):
            flash('Электронная почта не существует или недоступна!')
            return redirect(url_for('register'))

        # Регистрация пользователя
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно зарегистрирован! Теперь войдите.')
        return redirect(url_for('login'))

    return render_template('html/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Имя пользователя и пароль не могут быть пустыми!')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Вход выполнен успешно!')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль!')
            return redirect(url_for('login'))

    return render_template('html/login.html')


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = db.session.get(User, user_id) or abort(404)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)