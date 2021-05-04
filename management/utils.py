from core.models import Users, Passwords
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


def add_tests(name: str, path: str):
    """
    Unpack tests from archive to folder

    :param name: name of archive
    :param path: absolute path to directory with test and archive
    :return:

    """
    with zipfile.ZipFile(os.path.join(path, name)) as f:
        f.extractall(path)
    os.remove(os.path.join(path, name))
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            for j in os.listdir(os.path.join(path, i)):
                shutil.move(os.path.join(os.path.join(path, i), j), path)
            os.rmdir(os.path.join(path, i))


def create_ans(name: str, path_ans: str, path_test: str):
    if not os.path.exists(path_ans):
        os.mkdir(path_ans)
    for i in os.listdir(path_test):
        p = os.path.join(path_test, i)
        process = Popen(['python', name], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        with open(p, 'r') as f:
            process.communicate(input=f.read().encode())
        process.wait()
        output, _ = process.communicate()
        print(output.decode(), _.decode())
        with open(os.path.join(path_ans, i), 'w') as f:
            f.write(output.decode())


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
