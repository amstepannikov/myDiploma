from flask import render_template, Blueprint

from ..models import User
from ..configs import Config


# Создаем страницу/макета для администрирования
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')