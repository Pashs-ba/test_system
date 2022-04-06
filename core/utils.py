import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from threading import Thread
from .models import Competitions, Question, QuestionAns, StudentGroup
import openpyxl
from django.conf import settings
from django.conf import settings
import subprocess
from .models import *
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

def make_csv(request, competition, id, group):
    comp = Competitions.objects.get(pk=competition)
    group = StudentGroup.objects.get(pk=group)
    print(group)
    al = group.users.all().order_by('username')
    qa = comp.questions.all().order_by('name')
    with open(settings.BASE_DIR/f'media/{id}.txt', 'w', encoding="utf-8") as f:
        f.write(';')
        for quest in range(len(qa)): 
            f.write(f'{qa[quest].name};')
        f.write('\n')
        for user in range(len(al)):
            f.write(f'{al[user].username};')
            for quest in range(len(qa)):
                a = QuestionAns.objects.filter(user=al[user].pk, question=qa[quest].pk)
                if a:
                    if a[0].result:
                        if a[0].time:
                            delta = a[0].time
                            f.write(f'+ {delta};')
                    else:
                        if a[0].time:
                            delta = a[0].time
                            f.write(f'- {delta};')
                else:
                    f.write('0;')
            f.write('\n')


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

def sanya_run(string):
    a = subprocess.Popen([settings.BASE_DIR/'some'],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    a.communicate(input=string)
    a.wait()


def make_users():
    with open(settings.BASE_DIR/'all_res.txt', 'r') as f:
        data = list(map(lambda x: x.split(), f.read().split('\n')))
    for i in data:
        u = Users.objects.create_user(i[0], i[1])
        u.save()
        Passwords.objects.create(user=u, password=i[1]).save()