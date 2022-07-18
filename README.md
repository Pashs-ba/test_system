# Test System
![](https://camo.githubusercontent.com/e176bc131269431258122befa439e078ba62bc03cf0f4783b1029bcb5dcea049/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3337373641422e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/56ab15812d055930d7733010f09423049d50d9f9002a838e519825bf84ca1c2f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646a616e676f2d3039324532302e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/6492cf470515c2bbc1de05a4a01df5ab7861a5b7985f509d4450ce164858120f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f626f6f7473747261702d3736313046372e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d626f6f747374726170266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/1d04403d44ebbe655a8139af9c90183348c709b59f808543e286cc8c78bea0a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c696e75782d4643433632342e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6c696e7578266c6f676f436f6c6f723d303030)

Автоматическая тестирующая система для олимпиад и уроков информатики
 - [Установка](#установка)
    - [Локальная установка](#локальная-установка)
    - [Установка на сервере](#установка-на-сервер)
 - [Документация](#документация)
    - [Администраторам и учетелям](#администраторам-и-учетелям)
        - [Панель управления](#панель-управления)
            - [Управление юзерами](#управление-юзерами)
            - [Управление группами](#управление-группами)
            - [Управление вопросами](#управление-вопросами)
            - [Управление задачами](#управление-задачами)
            - [Управление соревнованиями](#управление-соревнованиями)
            - [Управление учителями](#управление-учителями)
        - [Панель ошибок](#панель-ошибок)
        - [Главная страница](#главная-страница)
        - [Внутренняя админ-панель](#внутренняя-админ-панель)
    - [Ученикам](#ученикам)
 - [Скриншоты](#скриншоты)

## Установка
### Локальная установка
*Я устанавливаю проект используя постгресс, если вы хотите любую другую бд, как ее настроить можно почитать в [Документации Django](https://docs.djangoproject.com/en/4.0/ref/databases/)*
1. Скачайте репозиторий
2. Установите библиотеки:
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
    ```
3. Создайте виртульное окружение:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
5. Зайдите в консоль базы данных:
    ```bash
    sudo -u postgres psql 
    ```
6. Создайте базу данных:
    ```sql
    CREATE DATABASE olympiad;
    ```
7. Создайте пользователя:
    ```sql
    CREATE USER olympiad_user WITH PASSWORD 'olympiad';
    ```
8. Настройте права юзера:
   ```sql
   ALTER ROLE olimpiad_user SET client_encoding TO 'utf8';
   ALTER ROLE olimpiad_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE olimpiad_user SET timezone TO 'UTC';
   ```
9. Предоставьте юзеру доступ в базу данных:
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE olympiad TO olympiad_user;
    ```
10. Выйдите из консоли базы данных:
    ```sql
    \q
    ```
11. Создайте файл конфигурации с названием `config.toml` и запишите в него следующие данные:
    ```toml
    [common]
    secret_key = "secret"
    debug = true
    [database]
    bd_name = "olimpiad"
    user = "olimpiad_user"
    password = "olimpiad"
    ```
12. Установите миграции;
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
13. Создайте суперпользователя:
    ```
    python manage.py createsuperuser
    ```
14. Запустите проект:
    ```
    python manage.py runserver
    ```
**После этих инструкций у вас запустится минимально рабочий проект. ЧАСТЬ ФИЧЕЙ НЕ БУДЕТ РАБОТАТЬ пока вы не установите Сelery и Redis инструкция по установке находится [вот здесь](https://hashsum.ru/celery-django-redis/)**

### Установка на сервер
Я использовал инструкцию по установке от [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-on-ubuntu-16-04), там все очень подробно описанно, кроме того что нужно обязательно создавать еще одного юзера, кроме рута.

## Документация
## Администраторам и учетелям
## Панель управления
### Управление юзерами
![](/screenshots/user.png)