from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


def upload(instance, filename):
    # print(instance)
    return f'contests/{filename}'
def content_file_name(instance, filename):
    return f'variant/{filename}'

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', unique=True, max_length=1024)

    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Admin', default=False)
    is_teacher = models.BooleanField('Teacher', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['pk']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.username

class Teachers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    password = models.CharField(max_length=1024, verbose_name='Password')
    
class Passwords(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    password = models.CharField(max_length=1024, verbose_name='Password')
    teacher = models.ForeignKey(Teachers, null=True, on_delete=models.CASCADE)


class Contests(models.Model):
    name = models.CharField(max_length=1024, verbose_name="Название", unique=True)
    description = models.TextField(null=True, verbose_name='Описание')

    time_limit = models.IntegerField(default=1000, verbose_name='Ограничение по времени, милисекунды')
    memory_limit = models.IntegerField(default=256, verbose_name='Ограничение по памяти, КB')

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
    file = models.FileField(null=True, blank=True, verbose_name='Файл')
    type = models.CharField(max_length=256, choices=QUESTION_TYPE, verbose_name='Тип')
    question = models.JSONField(null=True)
    teacher = models.ForeignKey(Teachers, null=True, on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Competitions(models.Model):
    name = models.CharField(max_length=1024, unique=True, verbose_name='Имя')
    description = models.TextField(null=True, verbose_name='Описание', blank=True)
    is_unlimited = models.BooleanField(default=False, verbose_name='Нет сроков')

    start_time = models.DateTimeField(null=True, verbose_name='Дата начала', blank=True)
    end_time = models.DateTimeField(null=True, verbose_name='Дата конца', blank=True)

    contests = models.ManyToManyField(Contests, blank=True, verbose_name='Задачи')
    questions = models.ManyToManyField(Question, blank=True, verbose_name='Вопросы')

    is_visible_result = models.BooleanField(null=True, blank=True, verbose_name="Показывать результаты", default=True)
    is_simulator = models.BooleanField(default=False, verbose_name='Является симулятором')
    is_final = models.BooleanField(default=False, verbose_name='Финальный результат')
    teacher = models.ForeignKey(Teachers, null=True, on_delete=models.CASCADE)
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
    ans = models.CharField(null=True, max_length=1024)
    result = models.BooleanField(null=True)
    time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.user} {self.question} {self.time}'


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
    teacher = models.ForeignKey(Teachers, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class VariantQuestionGenerator(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE,verbose_name='вопрос')
    generator = models.FileField(verbose_name='Генератор')
    var_count = models.IntegerField(null=True, verbose_name='Колличество вариантов')
    def __str__(self):
        return f'{self.question}'

class VariantQuestion(models.Model):
    data = models.JSONField()
    ans = models.JSONField()
    generator = models.ForeignKey(VariantQuestionGenerator, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(null=True, upload_to=content_file_name, blank=True)
    image = models.ImageField(null=True, upload_to=content_file_name,blank=True)

    def __str__(self):
        return f'{self.data} {self.ans}'
    


