from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


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
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True)
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=1024*1024*256)

    class Meta:
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'

    def __str__(self):
        return f'{self.name}'


class Competitions(models.Model):
    name = models.CharField(max_length=1024, unique=True, verbose_name='Имя')
    description = models.TextField(null=True, verbose_name='Описание', blank=True)
    participants = models.ManyToManyField(Users, null=True, verbose_name='Участники')
    is_unlimited = models.BooleanField(default=False, verbose_name='Нет сроков')
    start_time = models.DateTimeField(null=True, verbose_name='Дата начала', blank=True)
    end_time = models.DateTimeField(null=True, verbose_name='Дата конца', blank=True)
    contests = models.ManyToManyField(Contests, null=True, verbose_name='Задачи')

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return f'{self.name}'


class Solutions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    time = models.IntegerField(null=True)
    memory = models.IntegerField(null=True)
    result = models.CharField(max_length=1024, null=True)

    class Meta:
        verbose_name = 'Solution'
        verbose_name_plural = 'Solutions'

    def __str__(self):
        return f'{self.user} {self.contest} {self.result}'