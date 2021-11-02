import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from .models import Competitions


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
    if not competition.is_unlimited:
        now_local = timezone.datetime.now(competition.start_time.tzinfo)
    if competition.is_unlimited:
        return 'ОТКРЫТО'
    elif competition.start_time < now_local < competition.end_time:
        return 'ИДЕТ'
    elif competition.start_time > now_local:
        return 'НЕ НАЧАЛОСЬ'
    else:
        return 'ЗАКОНЧИЛОСЬ'



