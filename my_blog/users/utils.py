import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from my_blog import mail


def save_picture(form_picture):
    """
    Сохраняет фото пользователя
    :param form_picture: Файл изображения
    :return: Имя файла
    """
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'data/profile_pics', picture_fn)

    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """
    Отправляет письмо со ссылкой для сброса пароля пользователю
    :param user: Пользователь
    :return: None
    """
    token = user.get_reset_token()
    msg = Message('Запрос на сброс пароля', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''Чтобы сбросить пароль,
     перейдите по следующей ссылке: {url_for('users.reset_token', token=token, _external=True)}.
     Если вы не делали этот запрос, тогда просто проигнорируйте это письмо и никаких изменений не будет.'''
    mail.send(msg)