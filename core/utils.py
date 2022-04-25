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
import json

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
    al = group.users.all().order_by('username')
    qa = comp.questions.all().order_by('name')
    w = ""
    w+=';'
    for quest in range(len(qa)): 
        w+=f'{qa[quest].name};'
    w+='\n'
    for user in range(len(al)):
        w+=f'{al[user].username};'
        for quest in range(len(qa)):
            a = QuestionAns.objects.filter(user=al[user].pk, question=qa[quest].pk)
            if a:
                if a[0].result:
                    if a[0].time:
                        delta = a[0].time
                        w+=f'+ {delta};'
                else:
                    if a[0].time:
                        delta = a[0].time
                        w+=f'- {delta};'
            else:
                w+='0;'
        w+='\n'

    with open(settings.BASE_DIR/f'media/{id}.txt', 'w', encoding="utf-8") as f:
        f.write(w)

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
    for i in QuestionAns.objects.filter(question=Question.objects.get(pk=233)):
        q = json.loads(i.question.question)
        i.result = q['ans']==i.ans
        i.save()

