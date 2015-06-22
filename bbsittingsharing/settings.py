"""
Django settings for bbsittingsharing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from settings_specific import *

TEMPLATE_DEBUG = DEBUG

# Application definition

INSTALLED_APPS = (
    'bbsittingsharing',
    'bootstrapform',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bbsittingsharing.urls'
WSGI_APPLICATION = 'bbsittingsharing.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
LOCALE_PATHS = [BASE_DIR+'/locale/']
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.dirname(BASE_DIR)+'/pics/'
MEDIA_URL = '/pics/'

ACCOUNT_ACTIVATION_DAYS = 7
SEND_ACTIVATION_EMAIL = False
LOGIN_REDIRECT_URL = '/'
INCLUDE_REGISTER_URL = False
AUTH_USER_MODEL = 'bbsittingsharing.Parent'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.dirname(BASE_DIR)+'/static/'
