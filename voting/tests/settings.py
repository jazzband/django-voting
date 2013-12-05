import os

DIRNAME = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

SECRET_KEY = 'foo'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'voting',
    'voting.tests',
)
