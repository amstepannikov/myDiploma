# Дипломная работа
## Организация логинов и паролей пользователей информационной системы
WSGI-приложение  
(Web Server Gateway Interface - стандарт взаимодействия между python-программой,
выполняющейся на стороне сервера, и самим веб-сервером) 

### Начальный план:
1) Создание учетной записи:проверка сложности пароля, генератор надежного пароля.
2) Авторизация через сторонние системы, с помощью вконтакте, яндекса, гугла, гитхаб, сбер.
3) Хэширование паролей в БД
4) Защита от SQL-инъекций
5) Проверка паролей на утечки.(сайт have i been pwned)
6) Проверка пароля на фишинг
7) Регулярная смена пароля. Предупреждение пользователя, блокировка УЗ, если пароль не был сменен во время

### Структура файлов проекта
* my_blog - проект блога
  * data - данные
    * app.db - файл с sqlite базой блога
  * main - главный макет (blueprint)
    * routes.py - маршруты
  * posts - макеты постов
    * forms - формы
    * routes.py - маршруты
  * templates - шаблоны страниц HTML
    * reset_request.html - запрос на сброс пароля
    * reset_token.html - ввод нового пароля
  * users - макеты пользователей
    * forms - формы
    * routes.py - маршруты
    * utils.py - утилиты для работы с пользователями
  * __init__.py - инициализация проекта блога
  * configs.py - конфигурационный файл
  * models.py - модели (пользователи, посты)
* runner.py - запуск проекта

Устарело...  
* configs - конфигурации
* data - данные
  * app.db - файл с sqlite базой блога
* lib - вспомогательные функции
* logs - файлы логирования
* models - модель данных
* static - статические файлы
  * css - стили
  * images - изображения
* templates - шаблоны
  * css - шаблоны стилей
  * html - шаблоны html-страниц
  * js - JavaScript
* test - тестирование
  * fixture - фикстуры в pytest
* utils - вспомогательные скрипты и утилиты
  * works_db.py - утилита для работы с базой данных
  * create_secret_key.py - создает секретный ключ

### Используемый стек
* python 3.12
* Flask - микро-фреймворк для веб-разработки (`pip install Flask`)
  * Jinja2 - шаблонизатор
  * WTForms (Flask-WTF) - генератор WT-форм для Flask (`pip install -U Flask-SQLAlchemy`)
  * Flask-SQLAlchemy - работа с Базами Данных (`pip install -U Flask-SQLAlchemy`)
  * Flask-Mail - работа с почтой, основан на smtplib (`pip install Flask-Mail`)
  * Flask-Login - аунтификация (`pip install flask-login`)
  * Flask-Bcrypt - функционал для хеширования и проверки паролей (`pip install flask-bcrypt`)
  * Flask-Bootstrap - CSS фреймворк (`pip install flask-bootstrap`)
* SQLite - база данных, основанная на файле. Включен в Flask-SQLAlchemy.
* Pillow - работа с изображениями (`pip install Pillow`)
* ItsDangerous - обеспечение безопасности передачи данных (`pip install itsdangerous`)

### Источники
#### Статьи
[Проектирование простых приложений в Flask (хабр)](https://habr.com/ru/articles/275099/)  
[Мега-Учебник Flask (хабр)](https://habr.com/ru/articles/193242/)  
[Flask. Наполняем «флягу» функционалом (хабр)](https://habr.com/ru/articles/251415/)
[Начинающему веб-мастеру: делаем одностраничник на Bootstrap (хабр)](https://habr.com/ru/companies/ruvds/articles/350758/)

#### Документация
[Flask](https://flask.palletsprojects.com/en/stable/)  
[Jinja2](https://jinja.palletsprojects.com/en/stable/)  
[Flask WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)  
[Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)  
[Flask-Mail](https://flask-mail.readthedocs.io/en/latest/)  
[Flask-Login](https://flask-login.readthedocs.io/en/latest/)  
[Flask-Bootstrap](https://getbootstrap.com/docs/3.3/getting-started/)  
[Pillow](https://pillow.readthedocs.io/en/stable/)  
[ItsDangerous](https://itsdangerous.palletsprojects.com/en/stable/)  

#### Полезные ссылки
[Дизайнер SQL таблиц](https://sql.toad.cz/?)

### Разное
Загрузить библиотеки в requirements.txt (из каталога проекта):  
`pip freeze > requirements.txt`  
Инсталлировать все библиотеки из requirements.txt:  
`pip install -r requirements.txt`  

