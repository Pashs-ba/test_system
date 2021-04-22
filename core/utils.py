from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Users
from django.conf import settings
import string
import random


def upload_file(file: InMemoryUploadedFile):
    with open('users/{}'.format(file.name), 'wb') as f:
        for i in file.chunks():
            f.write(i)



