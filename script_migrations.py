from subprocess import call
from shutil import rmtree
import os

# удаляем папку с миграциями, если она есть
try:
    rmtree('migrations')
except Exception:
    pass

os.environ['FLASK_APP'] = 'runner.py'

# создаём папку с миграциями
command = "flask db init"
call(command, shell=True)

# создаём миграцию
command = "flask db migrate"
call(command, shell=True)

# выполняем миграцию
command = "flask db upgrade"
call(command, shell=True)
