from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Users
from django.conf import settings
import string
import random


def upload_file(file: InMemoryUploadedFile, folder: str):
    with open(f'{folder}', 'wb') as f:
        for i in file.chunks():
            f.write(i)



