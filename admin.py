from flask import Flask, render_template, request, redirect, url_for
#from flask.ext.sqlalchemy import SQLAlchemy

from project.forms import MessageForm
from configs.config import Config


app = Flask(__name__)
app.config.from_object(Config)
# инициализируем объект БД
#db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('html/index.html')


@app.route('/about')
def about():
    return render_template('html/about.html')


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


@app.route('/login')
def login():
    return render_template('html/login.html')


@app.route('/admin/')
def admin():
    if not loggedin:
        return redirect(url_for('login')) # если не залогинен, выполнять редирект на страницу входа
    return render_template('html/admin.html')


if __name__ == "__main__":
    loggedin = False
    app.run(host="localhost", port=5000, debug=True)