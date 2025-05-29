from flask_admin import Admin

from my_blog.models import User, Post, Role, RolesUsers
from my_blog import db, create_app
from .views import AdminPostView, AdminRoleView, AdminUserView, AdminUserRoleView, HomeAdminView


app = create_app()
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Создание админки
admin = Admin(app, name='my_blog', template_mode='bootstrap3', url='/', index_view=HomeAdminView(name='Утилиты'))
admin.add_view(AdminPostView(Post, db.session))
admin.add_view(AdminRoleView(Role, db.session))
admin.add_view(AdminUserRoleView(RolesUsers, db.session))
admin.add_view(AdminUserView(User, db.session))