# foodgram-project
![foodgram-project](https://github.com/mamontovdn/foodgram-project/workflows/foodgram-project/badge.svg)
### Адрес сайта
http://84.252.128.180
## Описание
Сайт является - базой кулинарных рецептов.
Пользователи могут создовать свои рецепты, читать рецепты других пользователей, 
подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также
создавать список покупок и загружать его в pdf формате.
Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx
## Как запустить

## Необходимое ПО

Docker: https://www.docker.com/get-started <br />
Docker-compose: https://docs.docker.com/compose/install/

## Инструкция по запуску
Сначало необходимо создать .env файл со следующем содержимым: <br />
```
EMAIL_HOST_USER = example@gmail.com # почта для отправки писем 
                                    # (используется для регистрации) 
EMAIL_HOST_PASSWORD = пароль от почты
SECRET_KEY = 'секретный ключ для csrf токена'
DB_ENGINE=django.db.backends.postgresql # Библиотека для использования PostgreSQL
DB_NAME= имя БД
POSTGRES_USER= имя postgres пользователя
POSTGRES_PASSWORD= пароль postgres пользователя
DB_HOST=db # название контейнера
DB_PORT=5432 # порт для подключения БД
```
Файл .env необходимо разместить в тойже директории, где и dockercompose-yaml <br /><br />
Затем, для запуска необходимо из корневой папки проекта ввести в консоль(bash или zsh) команду:
```
docker-compose up --build
```
Затем узнать id контейнера, для этого вводим
```
docker container ls
```
В ответ получаем примерно следующее
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                    NAMES
7262bd32bbcc   nginx:1.19.0             "/docker-entrypoint.…"   15 minutes ago   Up 15 minutes   0.0.0.0:80->80/tcp       mamontovdn_nginx_1
5182ca059029   mamontovdn/foodgram:v1   "/bin/sh -c 'gunicor…"   15 minutes ago   Up 15 minutes   0.0.0.0:8000->8000/tcp   mamontovdn_web_1
cc56c79a512c   postgres:12.4            "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes   5432/tcp                 mamontovdn_db_1
```
Нас интересует контейнер mamontovdn_web_1, заходим в него командой
```
docker exec -it <CONTAINER ID> bash
```
И делаем миграцию БД, и сбор статики
```
python manage.py migrate
python manage.py collectstatic
```
## Автор

* **Дмитрий Мамонтов** - https://github.com/MamontovDN
