from flask import url_for, redirect, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms.utils import unset_value

from my_blog.models import User, Post, Role, RolesUsers
from my_blog import db, create_app


class AdminMixin:
    """Миксин где определяем две функции, для проверки доступа к админки"""
    def is_accessible(self):
        """Если пользователь зарегистрировался, то проверяем есть ли у него роль admin"""
        if current_user.is_authenticated:
            return current_user.is_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """Если пользователь не зарегистрировался или у него нет роли, то выкидываем его в home"""
        return  redirect(url_for('main.home', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    """Проверка доступа к индексной страницы админки (с помощью миксина AdminMixin)"""
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    @expose('/email_check')
    def email_check(self):
        # Ваш код здесь
        print('Я в функции email_check')
        return redirect(url_for('admin.index'))

    @expose('/password_check')
    def password_check(self):
        # Ваш код здесь
        print('Я в функции password_check')
        return redirect(url_for('admin.index'))


class AdminPostView(AdminMixin, ModelView):
    """Создание вида таблицы Role, чтобы можно было редактировать данные в админке"""
    pass


class AdminRoleView(AdminMixin, ModelView):
    """Создание вида таблицы Role, чтобы можно было редактировать данные в админке"""
    pass


class AdminUserView(AdminMixin, ModelView):
    """Создание вида таблицы User, чтобы можно было редактировать данные в админке"""
    column_exclude_list = ('password',) # Не редактировать поле password
    # inline_models = (RolesUsers,) # Отображение роли пользователя на странице пользователя


class AdminUserRoleView(AdminMixin, ModelView):
    """Создание вида таблицы Role, чтобы можно было редактировать данные в админке"""
    form_columns = ('user_id', 'role_id')
    # inline_models = (Role,)