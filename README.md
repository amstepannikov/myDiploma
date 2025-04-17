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

### Структура каталогов проекта
* configs - конфигурации
* data - данные
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

### Используемый стек
* python 3.12
* Flask - фреймворк для веб-разработки
  * Jinja2 - шаблонизатор
  * WTForms (Flask-WTF) - генератор WT-форм для Flask
  * Flask-SQLAlchemy - работа с Базами Данных
  * Flask-Mail - работа с почтой (основан на smtplib)
  * Flask-Login - аунтификация
  * Flask-Bcrypt - функционал для хеширования и проверки паролей
* SQLite - база данных, основанная на файле

### Источники
#### Статьи
[Проектирование простых приложений в Flask (хабр)](https://habr.com/ru/articles/275099/)  
[Мега-Учебник Flask (хабр)](https://habr.com/ru/articles/193242/)
[Flask. Наполняем «флягу» функционалом](https://habr.com/ru/articles/251415/)

#### Документация 
[Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)

#### Полезные ссылки
[Дизайнер SQL таблиц](https://sql.toad.cz/?)