from my_blog import create_app
import locale

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

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
app = create_app()


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)