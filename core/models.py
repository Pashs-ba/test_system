from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class Users(AbstractBaseUser):
    username = models.CharField(max_length=1024)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_admin']
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        return self.username


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
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True)
    participants = models.ManyToManyField(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    contests = models.ManyToManyField(Contests)

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return f'{self.name}'


class Solutions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, on_delete=models.CASCADE)
    time = models.IntegerField(null=True)
    memory = models.IntegerField(null=True)
    result = models.CharField(max_length=1024, null=True)

    class Meta:
        verbose_name = 'Solution'
        verbose_name_plural = 'Solutions'

    def __str__(self):
        return f'{self.user} {self.contest} {self.result}'