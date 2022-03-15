import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from .models import Competitions, Question, QuestionAns, StudentGroup
import openpyxl
from django.conf import settings

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

def make_xl(request, competition, id):
    comp = Competitions.objects.get(pk=competition)
    group = StudentGroup.objects.get(competitions=comp)
    wb = openpyxl.Workbook()
    ws = wb.create_sheet("result")
    al = group.users.all().order_by('username')
    qa = comp.questions.all()
    for user in range(len(al)):
        ws.cell(row=user+2, column=1).value = al[user].username
        for quest in range(len(qa)):
            print(qa[quest].name)
            ws.cell(row=1, column=quest+2).value = qa[quest].name
            a = QuestionAns.objects.filter(user=al[user].pk, question=qa[quest].pk)
            ws.cell(row=user+2, column=quest+2, value="0")
            if a:
                if a[0].result:
                    ws.cell(row=user+2, column=quest+2, value="+")
                else:
                    ws.cell(row=user+2, column=quest+2, value="-")
    wb.save(str(settings.BASE_DIR / f'media/{id}.xlsx'))


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



