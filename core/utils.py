from pathlib import PosixPath
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Users
from django.conf import settings
import string
import random
import os


def upload_file(file: InMemoryUploadedFile, path):
    """
    Upload files from form

    :param file: request.FILE['<name>']
    :param path: way to save
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, file.name), 'wb') as f:
        for i in file.chunks():
            f.write(i)



