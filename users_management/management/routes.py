from flask import render_template, Blueprint

from ..models import User
from ..configs import Config


# Создаем страницу/макета для администрирования
management = Blueprint('management', __name__)


@management.route('/')
@management.route('/home')
def home():
    return render_template('home.html')