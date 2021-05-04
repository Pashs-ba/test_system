from core.models import Users, Passwords
from django.conf import settings
import string
import random
import zipfile
import os


def create_user():
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


def add_tests(name, path):
    """
    :param name: name of archive
    :param path: path to directory with test and archive
    :return:
    """
    with zipfile.ZipFile(os.path.join(path, name)) as f:
        f.extractall(os.path.join(settings.BASE_DIR, f'path'))