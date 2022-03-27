"""
Django settings for test_sys project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import toml


from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
data = toml.load(BASE_DIR/'config.toml')
# print(data['common']['secret_key'])
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = data['common']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = data['common']['debug']

ALLOWED_HOSTS = ['kussystem.ru', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'management',
    'crispy_forms',
    'api',
    'competition',
    'contest',
    'solutions',
    'questions',
    'widget_tweaks'

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'test_sys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'test_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': data['database']['bd_name'],
        'USER': data['database']['user'],
        'PASSWORD': data['database']['password'],
        'HOST': 'localhost',
        'PORT': '',
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.Users'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIRS = ['core/static',
               'static',
               # 'management/static'
               ]
STATIC_ROOT =os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'


USERNAME_LENGTH = 2
PASSWORD_LENGTH = 5
DATETIME_FORMAT = "%d.%m.%Y %H:%M"

ACCEPTABLE_FORMATS_IDEAL = ".py, .cpp"
ACCEPTABLE_LANGUAGES = {'Python 3.9': ['python', '.py'],
                        'MS C++ 19': ['c_cpp', '.cpp']}
PATH_TO_WIN_CPP = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\Tools\\VsDevCmd.bat"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

