# from admin import db, app
from ex3 import User, db, app
"""
Утилита для работы с базой данных
"""

def create_database():
    """
    Создание базы данных
    """
    app.app_context().push()
    db.create_all()


def create_user():
    """
    Создание пользователя
    """
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()


def select_user():
    """
    Чтение пользователя
    """
    users = User.query.all()
    print(users)
    print()


if __name__ == "__main__":
    """
    Главное меню
    """
    while True:
        print('Введите цифру:')
        print('1 - Создание базы данных')
        print('2 - Создание пользователей')
        print('3 - Чтение пользователей')
        print('0 - выход')
        print()

        i = input('Введите цифру меню: ')
        if i == '1':
            create_database()
        if i == '2':
            create_user()
        if i == '3':
            select_user()
        if i == '0':
            break

        print()