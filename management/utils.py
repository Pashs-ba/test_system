import subprocess
import ast
from core.models import Users, Passwords, Test, Contests, Solutions, VariantQuestion, VariantQuestionGenerator
from django.conf import settings
import string
import random
import zipfile
import os
import shutil
import platform
from subprocess import Popen, PIPE



def create_user() -> Passwords:
    """
    Create random user

    :return: login and password of user
    """
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(settings.PASSWORD_LENGTH))
    names = ['Tau', 'Mu', 'Ro', 'Alfa', 'Beta', 'Gamma', 'Omega', 'Epsilon', 'Eta', 'Nu', 'Pi', 'Dzeta', 'Psi']
    while True:
        name = ''.join(random.choice(names)+'-'+random.choice(names)+'-'+str(random.randint(1, 300)))
        # Generating unique names
        if not Users.objects.filter(username=name):
            user = Users.objects.create_user(name, password)
            a = Passwords(user=user, password=password)
            a.save()
            return a


def add_tests(name: str, path: str, pk: str):
    """
    Unpack tests from archive to folder

    :param name: name of archive
    :param path: absolute path to directory with test and archive
    :return:

    """
    with zipfile.ZipFile(os.path.join(path, name), 'r') as archive:
        for i in archive.namelist():
            if i[-1] != '/':
                with archive.open(i, 'r') as f:
                    a = f.read().decode()
                    test = Test(contest=Contests.objects.get(pk=pk), input=a)
                    test.save()
    os.remove(os.path.join(path, name))


def create_ans(pk: str, path_ideal: str):
    tests = Test.objects.filter(contest=Contests.objects.get(pk=pk))
    if '.py' in path_ideal:
        for i in tests:
            
            if platform.system() == 'Linux':
                process = Popen(['python3', path_ideal], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            else:
                process = Popen(['python', path_ideal], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            process.communicate(input=i.input.encode())
            process.wait()
            output, error = process.communicate()
            if error.decode() != '':
                i.is_error = True
            else:
                i.is_error = False
                i.output = output.decode()
            i.save()
    elif '.cpp' in path_ideal:
        if platform.system() == 'Windows':
            Popen(['cpp_compiler.cmd' , settings.PATH_TO_WIN_CPP, path_ideal, os.path.join(settings.BASE_DIR, f'media/DONT_TOUCH{pk}.exe')])
            for i in tests:
                process = Popen([os.path.join(settings.BASE_DIR, f'media/DONT_TOUCH{pk}.exe')], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                process.communicate(input=i.input.encode())
                process.wait()
                output, error = process.communicate()
                if error.decode() != '':
                    i.is_error = True
                else:
                    i.is_error = False
                    i.output = output.decode()
                i.save()
        else:
            Popen(['g++' , '-o', os.path.join(settings.BASE_DIR, f'media/DONT_TOUCH{pk}'), path_ideal])
            for i in tests:
                process = Popen([os.path.join(settings.BASE_DIR, f'media/DONT_TOUCH{pk}')], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                process.communicate(input=i.input.encode())
                process.wait()
                output, error = process.communicate()
                if error.decode() != '':
                    i.is_error = True
                else:
                    i.is_error = False
                    i.output = output.decode()
                i.save()


def get_tests(pk: str) -> list:
    dir = os.path.join(settings.BASE_DIR, pk)
    tests = []
    id = []
    ans = []
    test_dir = os.path.join(dir, 'tests')
    for i in os.listdir(test_dir):
        id.append(i)
        with open(os.path.join(test_dir, i), 'r') as f:
            tests.append(f.read())
    ans_dir = os.path.join(dir, 'ans')
    for i in os.listdir(ans_dir):
        with open(os.path.join(ans_dir, i), 'r') as f:
            ans.append(f.read())
    return list(zip(id, tests, ans))


def upload_tests(file, path):
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

def generate_variants_question(num, model_id, path_to):
    for i in range(num):
        process = Popen(f'media/{path_to}', stdout=PIPE, stderr=PIPE, stdin=PIPE)
        process.wait()
        stdout, stderr = process.communicate()
        ans = ast.literal_eval(stdout.decode())
        model = VariantQuestion(data=ans['data'], ans=ans['ans'], generator=VariantQuestionGenerator.objects.get(pk=model_id))
        if 'file' in ans.keys():
            model.file = ans['file']
        if 'image' in ans.keys():
            model.image = ans['image']
        model.save()