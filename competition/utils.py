import os

from django.conf import settings

from core.utils import upload_file

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
    if not os.path.exists(f'{request.user.pk}\\'):
        os.mkdir(f'{request.user.pk}\\')
    name = get_next_name(f'{request.user.pk}\\')
    ext = get_extension(lang)
    if code == '\n' or code == '':
        upload_file(request.FILES['file'], f'{request.user.pk}\\', name + ext)
    else:
        print(code)
        with open(f'{request.user.pk}\\' + name + ext, 'w') as f:
            f.write(code)
    return f'{request.user.pk}\\'+name+ext
