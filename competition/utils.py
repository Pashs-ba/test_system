import os
import platform
from django.conf import settings
from core.models import Solutions
from core.utils import upload_file
import subprocess

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


def save_solution(request, lang, code):
    if not os.path.exists(settings.MEDIA_ROOT+f'{request.user.pk}/'):
        os.mkdir(settings.MEDIA_ROOT+f'{request.user.pk}/')
    name = get_next_name(settings.MEDIA_ROOT+f'{request.user.pk}/')
    ext = get_extension(lang)
    if code == '\n' or code == '':
        upload_file(request.FILES['file'], settings.MEDIA_ROOT+f'{request.user.pk}/', name + ext)
    else:
        with open(settings.MEDIA_ROOT+f'{request.user.pk}/' + name + ext, 'w') as f:
            f.write(code)
    return f'{request.user.pk}/'+name+ext


def check_solution(solution: Solutions):
    print('process run')
    need = 'ChineseTester.exe'
    if platform.system() == 'Linux':
        need = '/home/pashs/ChineseTester'
    a = subprocess.Popen([need, str(solution.pk)],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    a.wait()
    b, c = a.communicate()
    try:
        print(b.decode())
    except Exception as e:
        print(b)
        print(e)
