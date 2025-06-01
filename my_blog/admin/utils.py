import os
import string
import secrets
import requests

from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from sqlalchemy import create_engine, Column, Integer, String, select

from my_blog import mail
from my_blog import db
from my_blog.models import User
from my_blog.users.utils import send_reset_email


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