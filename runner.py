from my_blog.admin import app
# import locale
import os

# from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand
# from app import app, db

# from models import *
# migrate = Migrate(app, db)
#
# # Инициализируем менеджер
# manager = Manager(app)
# # Регистрируем команду, реализованную в виде потомка класса Command
# manager.add_command('db', MigrateCommand)

# Устанавливаем параметры для использования авторизации по небезопасному протоколу http
# только для тестирования, для реальной работы по https необходимо их поставить в False '0'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# locale.setlocale(locale.LC_TIME, 'ru_RU')
# app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="localhost", port=5000, debug=True)