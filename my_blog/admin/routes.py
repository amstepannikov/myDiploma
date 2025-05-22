from flask_login import LoginManager, UserMixin, login_required, current_user
from flask import render_template, Blueprint
from flask_admin.contrib.sqla import ModelView

from my_blog.admin import admin
from my_blog.admin import app

# admins = Blueprint('admin', __name__)


@app.route('/admin/')
@login_required
def home():
     print(current_user.is_authenticated)
     return 'Home'