# -*- coding: utf-8 -*-

"""
Django settings for usd_cny project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import djcelery
djcelery.setup_loader()

reload(sys)
sys.setdefaultencoding('utf8')
DEFAULT_CHARSET = 'utf-8'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GIT_PATH = BASE_DIR
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
BASE_DIR = BASE_DIR + '/usd_cny'
sys.path.append(BASE_DIR + '/libs')
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

import djcelery
djcelery.setup_loader()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ff*54h%9-=6t_13$m!leg#9-gce%lw+y#wei*@=k@))udu0bjp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usd_cny.apps.transfer',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


ROOT_URLCONF = 'usd_cny.urls'

WSGI_APPLICATION = 'usd_cny.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # '/home/looen/workspace/coin2b/templates/',
    os.path.join(BASE_DIR, 'templates/').replace('\\', '/'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/').replace('\\','/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\','/')

STATIC_URL = '/static/'
# Additional locations of static files
base_locale_path = os.path.dirname(os.path.dirname(__file__))
LOCALE_PATHS = (
   os.path.join(base_locale_path, 'locale').replace('\\','/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("css", os.path.join(STATIC_ROOT,'css')),
    ("js", os.path.join(STATIC_ROOT,'js')),
    ("images", os.path.join(STATIC_ROOT,'images')),
    ("upload", os.path.join(STATIC_ROOT,'upload')),
    ("fonts", os.path.join(STATIC_ROOT,'fonts')),
    ("webuploader", os.path.join(STATIC_ROOT,'webuploader')),
    ("orders_qrcode", os.path.join(STATIC_ROOT,'orders_qrcode')),
)


BROKER_URL = 'sqla+sqlite:///celerydb.sqlite'
CELERY_TIMEZONE = TIME_ZONE

from  usd_cny.apps.transfer.tasks import get_balances
GET_BALANCE= get_balances.delay()