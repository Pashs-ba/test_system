import os
import platform
from django.conf import settings
from core.models import Solutions
from core.utils import upload_file
import subprocess
from django.conf import settings

def get_extension(lang: str):
    return settings.ACCEPTABLE_LANGUAGES[lang]


def get_next_name(path: str):
    if not os.listdir(path):
        return '0'
    else:
        return str(int(sorted(os.listdir(path))[-1].split('.')[0])+1)



def save_solution(request, lang, code):
    path = settings.MEDIA_ROOT+f'{request.user.pk}/'
    if not os.path.exists(path):
        os.mkdir(path)
    name = get_next_name(path)
    ext = get_extension(lang)
    if code == '\n' or code == '':
        upload_file(request.FILES['file'], path, name + ext)
    else:
        with open(path + name + ext, 'w') as f:
            f.write(code)
    return f'{request.user.pk}/'+name+ext


def check_solution(solution: Solutions):
    # print(str(settings.BASE_DIR))
    need = str(settings.BASE_DIR)+'/ChineseTester'
    a = subprocess.Popen([need, str(solution.pk), get_extension(solution.lang)],
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    a.wait()
    ans, err = a.communicate()
    if ans:
        print(ans.decode())
    if err:
        print(err.decode())

def get_ace_lang():
    d = {}
    for i in range(len(settings.ACCEPTABLE_LANGUAGES)):
        d[list(settings.ACCEPTABLE_LANGUAGES.keys())[i]] = settings.ACE_LANGUAGES[i]
    return d