from core.models import Users, Passwords, Test, Contests
from django.conf import settings
import string
import random
import zipfile
import os
import shutil
from subprocess import Popen, PIPE



def create_user() -> Passwords:
    """
    Create random user

    :return: login and password of user
    """
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(settings.PASSWORD_LENGTH))
    names = ['Gonros', 'Mauruin', 'Galagen', 'Gilvel', 'Karankyn', 'Borerys', 'Kalseth', 'Arrogen', 'Tenranel',
             'Caltharal', 'Moggazak', 'Ighazak', 'Skaghud', 'Graskogar', 'Algraz', 'Domesmashah', 'Domefist',
             'Doomskorchah', 'Goregashah', 'Battlecrasha']
    while True:
        name = ''.join(random.choice(names)+'_' for i in range(settings.USERNAME_LENGTH))
        name += str(random.randint(100, 1000))
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
                    test = Test(contest=Contests.objects.get(name=pk), input=f.read().decode())
                    test.save()
    os.remove(os.path.join(path, name))


def create_ans(pk: str, path_ideal: str):
    tests = Test.objects.filter(contest=Contests.objects.get(name=pk))
    for i in tests:
        process = Popen(['python', path_ideal], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        process.communicate(input=i.input.encode())
        process.wait()
        output, _ = process.communicate()
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