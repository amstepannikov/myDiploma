from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from my_blog.models import User, Post, Role
from my_blog import db
from my_blog import create_app


app = create_app()
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Создание админки
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Role, db.session))