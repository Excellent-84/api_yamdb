# Проект API YaMDb

API YaMDb собирает отзывы пользователей на различные произведения такие как фильмы, книги и музыка.

## Описание проекта:

API YaMDb позволяет работать со следующими сущностями:

  - JWT-токен (Auth): отправить confirmation_code на переданный email, получить JWT-токен в обмен на email и confirmation_code;
  - Пользователи (Users): получить список всех пользователей, создать пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учётной записи, изменить данные своей учётной записи;
  - Произведения (Titles), к которым пишут отзывы: получить список всех объектов, создать произведение для отзывов, информация об объекте, обновить информацию об объекте, удалить произведение. пользователя по username, получить данные своей учётной записи, изменить данные своей учётной записи;
  - Категории (Categories) произведений: получить список всех категорий, создать категорию, удалить категорию;
  - Жанры (Genres): получить список всех жанров, создать жанр, удалить жанр;
  - Отзывы (Review): получить список всех отзывов, создать новый отзыв, получить отзыв по id, частично обновить отзыв по id, удалить отзыв по id;
  - Комментарии (Comments) к отзывам: получить список всех комментариев к отзыву по id, создать новый комментарий для отзыва, получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id.

## Участники проекта:

[Excellent-84](https://github.com/Excellent-84) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля;

[BelovRV89](https://github.com/BelovRV89) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них;

[Александр Малахов](https://github.com/Richa9d) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.

## Используемые технологии:

  - Python 3.7+
  - Django 3.2
  - PyJWT 2.1.0
  - asgiref 3.6.0
  - attrs 22.2.0
  - certifi 2022.12.7
  - charset-normalizer 2.0.12
  - django-filter 22.1
  - djangorestframework 3.12.4
  - djangorestframework-simplejwt 5.2.2
  - flake8 6.0.0
  - idna 3.4
  - iniconfig 2.0.0
  - mccabe 0.7.0
  - packaging 23.0
  - pluggy 0.13.1
  - py 1.11.0
  - pycodestyle 2.10.0
  - pyflakes 3.0.1
  - pytest 6.2.4
  - pytest-django 4.4.0
  - pytest-pythonpath 0.7.3
  - pytz 2022.7.1
  - requests 2.26.0
  - rest-framework-simplejwt 0.0.1
  - sqlparse 0.4.3
  - toml 0.10.2
  - urllib3 1.26.15


## Начало работы:

  - Клонировать репозиторий, перейти в директорию с проектом:
```
git clone git@github.com:Excellent-84/api_yamdb.git
```
  - Установить виртуальное окружение, активировать его:
```
python -m venv venv
sourse venv/bin/activate
```
  - Перейти в директорию с приложением api_yamdb, установить зависимости:
```
pip install -r requirements.txt
```
  - Выполнить миграции:
```
cd api_yamdb/
python3 manage.py migrate
```
  - Запустить проект:
```
python3 manage.py runserver
```
  - Импорт БД из csv файла:
```
python3 manage.py import_data
```

## Пример запроса:

##### Регистрация нового пользователя:
POST запрос http://{ip-адрес}/api/v1/auth/signup/
```
{
    "email": "user@example.com",
    "username": "user"
}
```
##### Ответ:
```
{
    "email": "user@example.com",
    "username": "user"
}
```
##### Получение JWT-токена:
POST запрос http://{ip-адрес}/api/v1/auth/token/
```
{
    "confirmation_code": "str71ddb36c-xxxx-xxxx-xxxx-xxxxxxx",
    "username": "user"
}
```
##### Ответ:
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.XXXXXXX"
}
```
##### Добавление жанра
POST запрос http://{ip-адрес}/api/v1/genres/
```
{
    "name": "Комедия",
    "slug": "comedy"
}
```
##### Ответ
```
{
    "name": "Комедия",
    "slug": "comedy"
}
```
##### Получение списка всех жанров
GET запрос http://{ip-адрес}/api/v1/genres/

##### Ответ
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Комедия",
            "slug": "comedies"
        },
        {
            "name": "Комедия",
            "slug": "comedy"
        }
    ]
}
##### Удаление жанра
DELETE запрос http://{ip-адрес}/api/v1/genres/comedy/

##### Подробную версию запросов можно посмотреть по адресу:
http://{ip-адрес}/redoc/
