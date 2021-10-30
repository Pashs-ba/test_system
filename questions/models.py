from django.db import models


class Question(models.Model):
    type = models.CharField(max_length=256)
    name = models.CharField(max_length=1024)
    description = models.TextField()
    image = models.FileField(null=True)
