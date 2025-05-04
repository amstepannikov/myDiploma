import os
import string
import secrets

from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from my_blog import mail


def save_picture(form_picture) -> str:
    """
    Сохраняет фото пользователя
    :param form_picture: Файл изображения
    :return: Имя файла
    """
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/avatars', picture_fn)

    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def send_reset_email(user) -> None:
    """
    Отправляет письмо со ссылкой для сброса пароля пользователю
    :param user: Пользователь
    :return: None
    """
    token = user.get_reset_token()
    msg = Message('Запрос на сброс пароля', sender=current_app.config['DEFAULT_MAIL_SENDER'], recipients=[user.email])
    msg.body = f'''Чтобы сбросить пароль,
     перейдите по следующей ссылке: {url_for('users.reset_token', token=token, _external=True)}.
     Если вы не делали этот запрос, тогда просто проигнорируйте это письмо и никаких изменений не будет.'''
    mail.send(msg)


def generate_password(length=12) -> str:
    """
    Генератор паролей
    :param length: Длинна пароля
    :return: str
    Должен быть хотя бы один символ верхнего, нижнего регистра и пунктуации и не менее 3х цифр
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        # Для генерации пароля используем модуль secrets
        password = ''.join(secrets.choice(characters) for _ in range(length))
        if (any(i.islower() for i in password) and
            any(i.isupper() for i in password) and
            any(i in string.punctuation for i in password) and
            sum(i.isdigit() for i in password) >= 3):
                return password


def evaluate_password_strength(password) -> int:
    """
    Оценка сложностей паролей
    :param password: пароль
    :return: str
    Сложность считаем от 1 до 100

    - Длина пароля от 8 до 20 символов от 8 до 20 баллов
    - Наличие хотя бы одной заглавной буквы +10 баллов
    - Наличие хотя бы одной цифры +10 баллов
    - Наличие хотя бы одного специального символа +10 баллов
    - Отсутствие очевидных паттернов («password», «qwerty») +10 баллов
    - Количество уникальных символов > 70% от длины пароля +10 баллов
    - Использование все типы символов +20 баллов
    - Длина менее 8 символов -50% баллов
    """
    score = 1
    # Проверяем длину пароля
    if len(password) >= 8:
        score += min(len(password), 20)

    # Добавляем баллы за наличие разных видов символов
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special_char = any(char in string.punctuation for char in password)

    if has_uppercase:
        score += 10
    if has_lowercase:
        score += 10
    if has_digit:
        score += 10
    if has_special_char:
        score += 10

    # Бонус за использование всех типов символов
    if all([has_uppercase, has_lowercase, has_digit, has_special_char]):
        score += 20

    # Проверка на отсутствие простых шаблонов
    common_patterns = ["qwerty", "password", "admin"]
    if not any(pattern.lower() in password.lower() for pattern in common_patterns):
        score += 10

    # Уменьшаем оценку, если длина меньше минимально допустимой
    if len(password) < 8:
        score //= 2

    return min(score, 100)