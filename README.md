# Дипломная работа
## Организация логинов и паролей пользователей информационной системы "my_blog"
WSGI-приложение  
(Web Server Gateway Interface - стандарт взаимодействия между python-программой,
выполняющейся на стороне сервера, и самим веб-сервером) 

### План
#### Начальный план:
1) Создание учетной записи:проверка сложности пароля, генератор надежного пароля.
2) Авторизация через сторонние системы, с помощью вконтакте, яндекса, гугла, гитхаб, сбер.
3) Хэширование паролей в БД
4) Защита от SQL-инъекций
5) Проверка паролей на утечки.(сайт have i been pwned)
6) Проверка пароля на фишинг
7) Регулярная смена пароля. Предупреждение пользователя, блокировка УЗ, если пароль не был сменен во время

#### Текущий план:
Далее план будет расширяться, будет добавлен для каждого пункта процент готовности
* Создаём приложение my_blog
   * окна пользователя
     * ввод пароля        
       * войти через google (80% что будет)
       * войти через GitHub (50% что будет)
       * войти через VK (под вопросом)
       * ввод email
       * ввод пароля
       * переход в регистрацию
       * переход в Сброс пароля, через почту
     * регистрация
       * регистрация через google (80% что будет)
       * регистрация через GitHub (50% что будет)
       * регистрация через VK (под вопросом)
       * проверка email 
         * проверка на правильность формата
         * проверка на дубль (т.е. не должна уже быть в базе)
         * проверка на утечку через API [Have I Been Pwned API v3](https://haveibeenpwned.com/API/v3#BreachesForAccount) 
       * проверка пароля 
         * проверка на длину (например от 2х до ...) символов
         * проверка наличия типов символов (большая, маленькая, цифры, спец-символы)
         * проверка на идущие рядом символы (под вопросом)
         * проверка на утечку
           * через API (95% что будет)
           * через скачанный файл с хешами паролей (5% что будет)
         * проверка на SLQ-инъекции (не будет, только написать, что при использовании моделей инъекции сделать не получиться)
         * повторный ввод пароля, должен равен первому
         * генератор пароля (под вопросом)
         * отображение сложности пароля (под вопросом)
       * выбор аватарки, если не выбрать будет отображаться default.png
     * профиль пользователя
       * смена email (проверки см. регистрация)
       * смена аватарки
       * переход на ввод нового пароля
     * Сброс пароля, через почту
       * проверка email
         * проверка на правильность формата
         * проверка на наличия пользователя с данным email в базе
     * ввод нового пароля
       * проверка пароля
         * см. проверку при регистрации
         * проверка, что бы был не равен старому паролю
         * проверка, что бы был не равен списку старых паролей (под вопросом)
   * окна постов
      * все посты
      * посты только выбранного пользователя
      * один пост
        * если пост владельца, то возможность удалять, править
        * если пользователь админа, то возможность удалять, править (под вопросом)
      * создание поста
   * комментарии к постам (под вопросом)
   * лайки постам (под вопросом)
   * админка
     * тут ещё много вопросов
     * массовая проверка на утечки email
     * массовая проверка на утечки паролей
* фишинговый сайт (5% что будет)
  * не понятно куда складывать ворованные почту и пароли

#### Дополнительные задачи:
* прикрутить Flask-Bootstrap для стилей избавиться от старых стилей
* разобраться с админкой (там пока всё плохо)
* по возможности поправить код, а то его много просто скопированного с курса (мало ли запалят)

### Структура файлов проекта
* my_blog - проект блога
  * data - данные
    * app.db - файл с sqlite базой блога
  * errors - макеты ошибок (blueprint)
    * handlers.py - маршруты-обработчики ошибок
  * main - макет по умолчанию (blueprint)
    * routes.py - маршруты
  * posts - макеты постов (blueprint)
    * forms - формы
    * routes.py - маршруты
  * static - статические файлы
    * avatars - аватарки пользователей
    * css - шаблоны стилей
    * images - картинки
  * templates - шаблоны страниц HTML
    * errors - шаблоны ошибок
    * reset_request.html - отправка запроса на почту на сброс пароля
    * reset_token.html - ввод нового пароля через ссылку из почты
    * users - макеты пользователей (blueprint)
      * forms - формы
      * routes.py - маршруты
      * utils.py - утилиты для работы с пользователями
    * __init__.py - инициализация проекта блога
    * configs.py - конфигурационный файл
    * models.py - модели (пользователи, посты)
* runner.py - запуск проекта
* Procfile - файл для развёртывания приложений в облачных хостиногов, таких, как Heroku...
* requirements.txt - список используемых библиотек, используется для их развертывания
* runtime - указания версии python

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
  * Flask-Dance - авторизация через OAuth (`pip install flask-dance google-auth-oauthlib`)
  * Flask-Gunicorn - WSGI-сервер для Python-Flask веб-приложений (`pip install gunicorn`)
  * Flask-Admin - административный интерфейс (`pip install Flask-Admin`)
* SQLite - база данных, основанная на файле. Включен в Flask-SQLAlchemy.
* Pillow - работа с изображениями (`pip install Pillow`)
* ItsDangerous - обеспечение безопасности передачи данных (`pip install itsdangerous`)

### Источники
#### Статьи
[Проектирование простых приложений в Flask (хабр)](https://habr.com/ru/articles/275099/)  
[Мега-Учебник Flask (хабр)](https://habr.com/ru/articles/193242/)  
[Flask. Наполняем «флягу» функционалом (хабр)](https://habr.com/ru/articles/251415/)  
[Начинающему веб-мастеру: делаем одностраничник на Bootstrap (хабр)](https://habr.com/ru/companies/ruvds/articles/350758/)  
[Flask-Admin (хабр)](https://habr.com/ru/articles/148765/)  

#### Документация используемых библиотек
[Flask](https://flask.palletsprojects.com/en/stable/)  
[Jinja2](https://jinja.palletsprojects.com/en/stable/)  
[Flask WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)  
[Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)  
[Flask-Mail](https://flask-mail.readthedocs.io/en/latest/)  
[Flask-Login](https://flask-login.readthedocs.io/en/latest/)  
[Flask-Bootstrap](https://getbootstrap.com/docs/3.3/getting-started/)  
[Flask-Dance](https://flask-dance.readthedocs.io/en/latest/#)  
[Flask-Gunicorn](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/)  
[Flask-Admin](https://flask-admin.readthedocs.io/en/stable/)  
[Pillow](https://pillow.readthedocs.io/en/stable/)  
[ItsDangerous](https://itsdangerous.palletsprojects.com/en/stable/)  

#### Полезные ссылки
[Дизайнер SQL таблиц](https://sql.toad.cz/?)  
[DB Browser for SQLite - программа просмотра базы SQLite](https://sqlitebrowser.org/dl/)  

### Разное
Загрузить библиотеки в requirements.txt (из каталога проекта):  
`pip freeze > requirements.txt`  
Инсталлировать все библиотеки из requirements.txt:  
`pip install -r requirements.txt`  

### Схема данных  
#### users - таблица пользователей  
id - INTEGER, PK, NOT NULL - идентификатор пользователя  
username - VARCHAR(20) NOT NULL - имя  
email - VARCHAR(100), NOT NULL - почта, он же логин  
password - VARCHAR(60) - хеш пароля, может быть пустым, если авторизация через внешние ресурсы (если реализую эту авторизацию)  
first_name - VARCHAR(60) - ну пусть будет  
last_name - VARCHAR(60)  
avatar - VARCHAR(20) - имя-номер файла аватарки, если пусто то my_blog/static/avatars/default.png 

### posts - таблица постов
id - INTEGER, PK, NOT NULL - идентификатор поста  
title - VARCHAR(100), NOT NULL - заголовок  
date_posted - DATETIME, NOT NULL - время создания  
content - TEXT, NOT NULL - текст поста  
user_id - INTEGER, FK, NOT NULL - идентификатор пользователя  