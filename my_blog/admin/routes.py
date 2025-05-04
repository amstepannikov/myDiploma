from flask_login import LoginManager, UserMixin, login_required
from flask import render_template, Blueprint


# @admin.route('/admin/')
# @login_required
# def admin():
#     return render_template('admin.html')