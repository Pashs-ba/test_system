from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


def upload(instance, filename):
    # print(instance)
    return f'contests/{filename}'


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', unique=True, max_length=1024)

    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Admin', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.username


    
class Passwords(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    password = models.CharField(max_length=1024, verbose_name='Password')


class Contests(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Название", unique=True)
    description = models.TextField(null=True, verbose_name='Описание')

    time_limit = models.IntegerField(default=1, verbose_name='Ограничение по времени, секунды')
    memory_limit = models.IntegerField(default=256, verbose_name='Ограничение по памяти, MB')

    input = models.TextField(verbose_name='Формат ввода', null=True)
    output = models.TextField(verbose_name='Формат вывода', null=True)

    ideal_ans = models.FileField(verbose_name='Идеальное решение', upload_to=upload)
    checker = models.FileField(verbose_name="Чекер", upload_to=upload, null=True)

    class Meta:
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    QUESTION_TYPE = [
        ('0', 'Свободный ответ'),
        ('1', 'Один вариант ответа'),
        ('2', 'Несколько ответов'),
    ]

    name = models.CharField(max_length=1024, verbose_name='Имя')
    description = models.TextField(verbose_name='Текст задания')
    image = models.FileField(null=True, blank=True, verbose_name='Изображение')
    type = models.CharField(max_length=256, choices=QUESTION_TYPE, verbose_name='Тип')
    question = models.JSONField(null=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.name}'


class Competitions(models.Model):
    name = models.CharField(max_length=1024, unique=True, verbose_name='Имя')
    description = models.TextField(null=True, verbose_name='Описание', blank=True)
    participants = models.ManyToManyField(Users, null=True, verbose_name='Участники')
    is_unlimited = models.BooleanField(default=False, verbose_name='Нет сроков')
    start_time = models.DateTimeField(null=True, verbose_name='Дата начала', blank=True)
    end_time = models.DateTimeField(null=True, verbose_name='Дата конца', blank=True)
    contests = models.ManyToManyField(Contests, null=True, blank=True, verbose_name='Задачи')
    questions = models.ManyToManyField(Question, null=True, blank=True, verbose_name='Вопросы')

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return f'{self.name}'


class Solutions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    lang = models.CharField(verbose_name="Язык", null=True, max_length=1024)
    time = models.FloatField(null=True)
    memory = models.IntegerField(null=True)
    result = models.CharField(max_length=1024, null=True)
    file_name = models.CharField(max_length=1024, null=True)
    date = models.DateTimeField(verbose_name='Дата посылки', null=True, auto_now=True)

    class Meta:
        verbose_name = 'Solution'
        verbose_name_plural = 'Solutions'

    def __str__(self):
        return f'{self.user} {self.contest} {self.result}'


class QuestionAns(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    number_of_attempt = models.IntegerField(default=1)
    result = models.BooleanField()


class Test(models.Model):
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField(null=True)
    is_example = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)

class StudentGroup(models.Model):
    name= models.CharField(verbose_name="Имя", max_length=1024)
    users = models.ManyToManyField(Users, verbose_name="Пользователи")
    competitions = models.ManyToManyField(Competitions, verbose_name="Соревнования")

    def __str__(self):
        return self.name