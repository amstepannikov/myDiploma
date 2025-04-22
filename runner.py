from users_management import create_app
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

app = create_app()


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)