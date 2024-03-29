![image](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![image](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)<br>
[![](https://img.shields.io/badge/python-3.7.0-green)](https://img.shields.io/badge/python-3.7.0-green)
[![](https://img.shields.io/badge/Django-2.2.16-yellowgreen)](https://img.shields.io/badge/Django-2.2.16-yellowgreen)
[![](https://img.shields.io/badge/DRF-3.12.4-brightgreen)](https://img.shields.io/badge/DRF-3.12.4-brightgreen)
[![](https://img.shields.io/apm/l/vim-mode.svg)](https://choosealicense.com/licenses/mit/)


# Проект YaMDb
### Описание проекта
Данное API предоставляет доступ к сервису YaMDb.
Проект YaMDb собирает отзывы пользователей на произведения.<br>
API позволяет оставлять и просматривать отзывы и комментарии к произведениям, просматривать произведения по категориям и жанрам.
Пользователи с некоторыми пользовательскими ролями имеют расширенные права на управление контентом, включая создание произведений, жанров и категорий, удаление и правка отзывов и комментариев.<br>

### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь `user` — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям, может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор `moderator` — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор `admin` — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Документация API

> Документация доступна по адресу: `/redoc`

### Самостоятельная регистрация новых пользователей

1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`.
2. Сервис YaMDB отправляет письмо с кодом подтверждения `(confirmation_code)` на указанный адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.<br>
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором
Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.<br>
После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/`, в ответ ему должно прийти письмо с кодом подтверждения.<br>
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

### Ресурсы API YaMDb
- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Инструкция по запуску проекта на своей машине:
1. Скачиваем репозиторий
2. Устанавливаем и активируем виртуальное окружение  
3. Устанавливаем зависимости `pip install -r requirements.txt`
4. Запустить миграции `python manage.py migrate`  
5. Создать суперюзера для доступа к админке `python manage.py createsuperuser`
6. Запуск проекта `python manage.py runserver`

### Инструкция по созданию dummy data
> Для создания dummy data используйте кастомную management-команду `python manage.py create_dummy_data`
