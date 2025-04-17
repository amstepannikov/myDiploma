from flask import Flask, render_template, request, redirect, url_for

from project.forms import MessageForm
from configs.config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.errorhandler(404)
def http_404_handler(error):
    return "<p>HTTP 404 Error Encountered</p>", 404

@app.errorhandler(500)
def http_500_handler(error):
    return "<p>HTTP 500 Error Encountered</p>", 500


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


@app.route('/user/<id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)