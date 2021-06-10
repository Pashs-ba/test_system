from pathlib import PosixPath
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Users
from django.conf import settings
import string
import random
import os
from .models import Competitions
from django.utils import timezone


def upload_file(file: InMemoryUploadedFile, path, name):
    """
    Upload files from form

    :param file: request.FILE['<name>']
    :param path: way to save
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, name), 'wb') as f:
        for i in file.chunks():
            f.write(i)


def competition_status(competition: Competitions):
    now_local = timezone.datetime.now(competition.start_time.tzinfo)
    if competition.is_unlimited:
        return 'ОТКРЫТО'
    elif competition.start_time < now_local < competition.end_time:
        return 'ИДЕТ'
    elif competition.start_time > now_local:
        return 'НЕ НАЧАЛОСЬ'
    else:
        return 'ЗАКОНЧИЛОСЬ'


def get_extension(lang: str):
    for i in settings.ACCEPTABLE_LANGUAGES:
        if lang in settings.ACCEPTABLE_LANGUAGES[i]:
            return settings.ACCEPTABLE_LANGUAGES[i][1]
    raise ValueError('Lang not found')


def get_next_name(path: str):
    max = 0
    for i in os.listdir(path):
        if int(i.split('.')[0]) > max:
            max = int(i.split('.')[0])

    return str(max+1)