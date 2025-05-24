from flask import url_for, redirect, request
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from my_blog.models import User, Post, Role
from my_blog import db
from my_blog import create_app


app = create_app()
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class AdminMixin:
    """Миксин где определяем две функции, для проверки доступа к админки"""
    def is_accessible(self):
        """Если пользователь зарегистрировался, то проверяем есть ли у него роль admin"""
        if current_user.is_authenticated:
            return current_user.is_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """Если пользователь не зарегистрировался или у него нет роли, то выкидываем его в home"""
        return  redirect(url_for('main.home', next=request.url))


class AdminView(AdminMixin, ModelView):
    """Проверка доступа к таблицам админки (с помощью миксина AdminMixin)"""
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    """Проверка доступа к индексной страницы админки (с помощью миксина AdminMixin)"""
    pass


# Создание админки
admin = Admin(app, name='my_blog', template_mode='bootstrap3', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Role, db.session))