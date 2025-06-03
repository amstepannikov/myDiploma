from flask import url_for, redirect, request, render_template
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from my_blog.admin.utils import checking_passwords_leaks, checked_compromised_emails


class AdminMixin:
    """Миксин где определяем две функции, для проверки доступа к админки"""

    def is_accessible(self):
        """Если пользователь зарегистрировался, то проверяем есть ли у него роль admin"""
        if current_user.is_authenticated:
            return current_user.is_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """Если пользователь не зарегистрировался или у него нет роли, то выкидываем его в home"""
        return redirect(url_for('main.home', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    """Проверка доступа к индексной страницы админки (с помощью миксина AdminMixin)"""

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    @expose('/email_check')
    def email_check(self):
        # Ваш код здесь
        results = checked_compromised_emails()
        return self.render('admin/index.html', results_email_check=results)

    @expose('/password_check')
    def password_check(self):
        results = checking_passwords_leaks()
        return self.render('admin/index.html', results_password_check=results)


class AdminPostView(AdminMixin, ModelView):
    """Создание вида таблицы Role, чтобы можно было редактировать данные в админке"""
    pass


class AdminRoleView(AdminMixin, ModelView):
    """Создание вида таблицы Role, чтобы можно было редактировать данные в админке"""
    column_list = ['name', 'description']
    can_create = False
    can_edit = False
    can_delete = False


class AdminUserView(AdminMixin, ModelView):
    """Создание вида таблицы User, чтобы можно было редактировать данные в админке"""

    # Не отображать поле password
    column_exclude_list = ('password',)
    # Запрещаем создавать запись
    can_create = False
    # Разрешаем редактировать только поле is_active
    form_edit_rules = ('is_active', )