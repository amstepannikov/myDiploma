from functools import wraps

from flask import g, flash, redirect, url_for, request


def requires_login(f):
    """
    В представлении объявляется Blueprint — объект схемы модуля, в свойствах которого указывается url_prefix,
     который будет подставляться в начале любого URLа, указанного в route.
     Также в представлении используется метод формы form.validate_on_submit,
     выдающий истину для метода HTTP POST и валидной формы.
     После успешного входа пользователь перенаправляется на страницу профиля (/users/me).
     Для предотвращения доступа неавторизованных пользователей создаётся специальный декоратор в файле
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)

    return decorated_function