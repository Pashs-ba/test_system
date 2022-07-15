from test_sys.celery import app
from django.conf import settings
from .models import Competitions, StudentGroup, QuestionAns

from celery import shared_task
import datetime

@shared_task
def make_csv(competition, group):
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
    name = str(datetime.datetime.now().time()).replace('.', '').replace(':', '')
    with open(settings.BASE_DIR/f'media/{name}.txt', 'w', encoding="utf-8") as f:
        f.write(w)
    return name


