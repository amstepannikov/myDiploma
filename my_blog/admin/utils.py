import csv
import requests

from my_blog import db
from my_blog.models import User
from my_blog.users.utils import send_reset_email


def checked_compromised_emails() -> list[list[int | str]]:
    """
    Проверка почты на утечки
    :return: список пользователей
    """

    # Берем только активные аккаунты и тип my_blog
    users = db.session.query(User).filter_by(is_active=True).filter_by(auth_type='my_blog').all()

    with open('my_blog/data/leaked_emails.csv', encoding='utf-8') as file:
        leaked_emails = set(line.strip().lower() for line in file if '@' in line)

    checking_email = []
    for user in users:

        if user.email in leaked_emails:
            lst = [user.username, user.email]
            # Если НЕ тестовая почта, то отправляем сообщение на почту
            if 'test@' in user.email:
                lst.append('тестовая почта')
            else:
                lst.append('письмо отправлено')
                email_message = f'Уважаемый {user.username}! Администрация my_blog выявила, что ваш email скомпрометирован, просим сменить ваш пароль\n'
                send_reset_email(user, email_message)
            checking_email.append(lst)
    return checking_email


def checking_passwords_leaks() -> list[list[int | str]]:
    """
    Проверка паролей на утечки
    :return: список пользователей
    """

    def check_response(hashes, hash_to_check):
        hashes_list = hashes.splitlines()
        for hsh in hashes_list:
            line_parts = hsh.split(':')
            found_hash = line_parts[0].strip()
            occurrences = int(line_parts[1])

            if found_hash == hash_to_check:
                return occurrences
        return 0

    # Берем только активные аккаунты и тип my_blog
    users = db.session.query(User).filter_by(is_active=True).filter_by(auth_type='my_blog').all()
    checking_users = []
    for user in users:
        lst = [user.username, user.email]

        password_sha1 = user.password.upper()
        # Первые 5 символов хэша отправляются на API
        first_5_chars = password_sha1[:5]
        remaining_hash = password_sha1[5:]
        try:
            response = requests.get(f'https://api.pwnedpasswords.com/range/{first_5_chars}')

            # Проверяем полный хэш среди полученных значений
            count = check_response(response.text, remaining_hash)
            lst.append(count)
        except Exception:
            lst.append('Error API')
            lst.append('')
        else:
            # Если НЕ тестовая почта и нужно менять пароль, то отправляем сообщение на почту
            email_message = ''
            if count > 10:
                lst.append('надо обязательно сменить пароль')
                email_message = f'Уважаемый {user.username}! Администрация my_blog выявила, что ваш пароль очень уязвим и вам обязательно нужно его сменить\n'
            elif count:
                lst.append('можно сменить пароль')
                email_message = f'Уважаемый {user.username}! Администрация my_blog выявила, что ваш пароль уязвим и вам желательно его сменить\n'
            else:
                lst.append('пароль менять не нужно')

            if 'test@' in user.email:
                lst.append('тестовая почта')
            elif count:
                lst.append('письмо отправлено')
                send_reset_email(user, email_message)
            else:
                lst.append('письмо не нужно')

        checking_users.append(lst)
    return checking_users
