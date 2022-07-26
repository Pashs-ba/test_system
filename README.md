# Test System
![](https://camo.githubusercontent.com/e176bc131269431258122befa439e078ba62bc03cf0f4783b1029bcb5dcea049/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3337373641422e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/56ab15812d055930d7733010f09423049d50d9f9002a838e519825bf84ca1c2f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646a616e676f2d3039324532302e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d646a616e676f266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/6492cf470515c2bbc1de05a4a01df5ab7861a5b7985f509d4450ce164858120f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f626f6f7473747261702d3736313046372e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d626f6f747374726170266c6f676f436f6c6f723d666666)
![](https://camo.githubusercontent.com/1d04403d44ebbe655a8139af9c90183348c709b59f808543e286cc8c78bea0a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c696e75782d4643433632342e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6c696e7578266c6f676f436f6c6f723d303030)

Автоматическая тестирующая система для олимпиад и уроков информатики.

Если у вас есть вопросы можете написать [мне](https://t.me/Pashs_ba) или в наш аккаунт в тг [@rcomrad](https://t.me/rcomrad)
 - [Установка](#установка)
    - [Локальная установка](#локальная-установка)
    - [Установка на сервере](#установка-на-сервер)
 - [Документация](#документация)
    - [Администраторам и учителям](#администраторам-и-учителям)
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
        - [Соревнования](#соревнования)
        - [Задачи](#задачи)
        - [Обратная связь](#обратная-связь)
- [Скриншоты](#скриншоты)

## Установка
### Локальная установка
*Я устанавливаю проект используя постгресс, если вы хотите любую другую бд, о том как ее настроить можно почитать в [Документации Django](https://docs.djangoproject.com/en/4.0/ref/databases/)*
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
*После этих инструкций у вас запустится минимально рабочий проект.*

*ЧАСТЬ ФИЧЕЙ НЕ БУДЕТ РАБОТАТЬ пока вы не установите Сelery и Redis инструкция по установке находится [вот здесь](https://hashsum.ru/celery-django-redis/)*

### Установка на сервер
Если вы хотите установить проект на сервер то используйте инструкцию от [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04-ru).

## Документация
## Администраторам и учителям
## Панель управления
*NB! Все таблицы системы управление сортируемы*
### Управление юзерами
![](/screenshots/admin/user.png)
*Система не позовляет самотсояетльно регестрироваться ученикам, вместо этого она сама генерирует готовых юзеров и пароли*

Для того что бы создать юзеров нажмите на соответствующую кнопку в панели управления и выберите желаемое количество. Что бы увидеть новых юзеров надо перезагрузить страницу.

Система создаст таблицу в которой будут хранится все юзеры, их пароли, групппы и учетеля.

У каждого юзера можно менять имя.

Кнопка "Создать таблицу юзеров" создает выгрузку всех юзеров в .csv файл.

### Управление группами
![](/screenshots/admin/group.png)
Группы позволяют соеденять учеников и соревнования. Панель управления группами аналогична всем остальным панелям системы

### Управление вопросами
![](/screenshots/admin/question_page.png)
Вопросы это задания которые не требуют сложной проверки при ответе.

Страница впросов содержит список всех существующих вопросов и позволяет менять и смтореть их.

Существует 3 вида вопросов:
- Вопрос с одним вариантом ответа
- Вопрос с несколькими вариантами ответа
- Вопрос со свободным ответом


![](/screenshots/admin/q_create.png)
При создании вопроса необходимо обязательно выбрать его тип. Кроме этого можно загрузить картинку и файл и указать теги.
С помощью тегов вопросы можно искатьв панели создания соревнований (что бы искать по тегам нужно в строке поиска написать #тег)

### Управление задачами
![](screenshots/admin/contests.png)
*Кнопка Загрузить с Codeforces находится в разработке*

Страница задач содержит список всех существующих задач.


![](/screenshots/admin/mathjax.png)
При создании задачи в полях описания, примера входа и выхода можно использовать Latex. Весь ввод удет сражу же рендерится внизу.

Кроме этого для каждой задачи нужно загрузить идеальное решение (на Python или C++), чекер и набор тестов в .zip. [Пример набора этих файлов](https://drive.google.com/drive/folders/1aZ9a05B2iTO3sDAPxirYfF5DPlr7O5Gq?usp=sharing)

После создания задачи создается страница управления задачей. Она аналогична странице создания за исключением блока тестов.
![](/screenshots/admin/tests.png)
В этом блоке указаны тесты и ответы на них (ответы генерируются идеальным решением и при проблеме с ним вместо ответов будет ошибка)

Тесты можно сделать примерами, и тогда они будут показаны на странце задач.

### Управление соревнованиями

![](/screenshots/admin/competition.png)
Соревнования это набор задач и вопросов

![](/screenshots/admin/comp_create.png)
При создании соревнований можно указать время начала и конца или бессрочный режим.

У соревнований существует 4 различных режима:
- Стандартный - пользлватель видит ответы на вопросы и может отвечать на них только один раз.
- Скрытый - пользователь не видит ответы на вопросы и может отвечать на них любое количество раз
- Симулятор КЕГЭ - интерфейс меняется на симуляцию КЕГЭ (*Поддерживает только вопросы!*)
- Учебный - пользователь видит ответы на вопросы и может отвечать на них любое количество раз
  
*Результаты решений задач видны всегда!*

### Управление учителями
![](/screenshots/admin/teachers.png)
*Эта функция доступна только администраторам!*

Учителя, в отличии от администраторов, видят только свои задачи, группы и учеников. Это позволяет им более точно следить за ними.

Создание учителей не отличается от создания учеников.

## Панель ошибок
![](/screenshots/admin/error.png)
Во время соревнований у пользователей могут возникать проблемы, о которых они могут написать вам в эту панель.

Количество текущих нерешенных проблем указано на панели сверху.
![](/screenshots/admin/ans.png)
На странице ответа вы можете изменить соревнование, написать ответ, превратить ответ в оповещение всем участникам соревнования и выбрать тип этого оповещения.

Если у пользователя есть проблемы со входом в систему то вместо его имени будет отображаться идентефикатор сессии.

*Вы можете ввести только один ответ!*

![](/screenshots/admin/alert.png)
Кроме ответа на конкретный вопрос можно сделать оповещения для всех участников соревнования.
Тип оповещения влияет только на его цвет (цвета взяты с [бутстрапа](https://getbootstrap.com/docs/4.0/components/alerts/#examples))

## Главная страница
![](/screenshots/admin/main_page.png)
На главной странице администраторы могут просматривать статистику соревнований.

Таблица доступна в 2 видах:
- Таблица на сайте
- CSV-файл (доступен только если установлен Celery/Redis)

## Внутренняя админ-панель
Внутренняя админ-панель находится по стандартному адресу в Django и доступна только администраторам.

## Ученикам
## Соревнования
![](/screenshots/students/student_copm.png)
Вид страницы соренований зависит от его типа (вот [здесь](#управление-соревнованиями) описаны типы)

## Задачи
![](/screenshots/students/user_con.png)
На странице задач можно увидеть описание, примеры ввода и ваши решения.

При посылке задач, она проверяется на скрытых от участника тестах.

Вердикт тестирования можно увидеть в блоке решений или на главной странице.

Существует 5 возможных вердиктов:
- *OK* - задача выполнена верно
- *TL* - Задача превысила лимит времени
- *ML* - Задача превысила лимит памяти
- *WA* - Задача выполнена неверно
- *CE* - Ошибка компиляции

## Обратная связь
![](/screenshots/students/err_ans.png)
При возникновении проблем вы можете написать в форму обратной связи которая находится на верхней панели. Жюри может не отвечать на ваш вопрос(или ответить бессодержательно), если посчитеат что ответ может дать подсказку по решению.

## Скриншоты
![](/screenshots/common/alert.png)
![](/screenshots/common/ans.png)
![](/screenshots/common/competition.png)
![](/screenshots/common/comp_create.png)
![](/screenshots/common/contests.png)
![](/screenshots/common/create_error.png)
![](/screenshots/common/error.png)
![](/screenshots/common/err_ans.png)
![](/screenshots/common/group.png)
![](/screenshots/common/list_errors.png)
![](/screenshots/common/login.png)
![](/screenshots/common/main.py)
![](/screenshots/common/main_admin.png)
![](/screenshots/common/main_page.png)
![](/screenshots/common/manage.png)
![](/screenshots/common/mathjax.png)
![](/screenshots/common/question_page.png)
![](/screenshots/common/q_create.png)
![](/screenshots/common/student_copm.png)
![](/screenshots/common/student_main.png)
![](/screenshots/common/teachers.png)
![](/screenshots/common/tests.png)
![](/screenshots/common/user.png)
![](/screenshots/common/user_con.png)