from following_level.local_settings import *

import os
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Paris'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '6@wy+1yh51cih)u_x5i!u9m7@=)+1b#+22irz60nak=c7b=!=8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'stats.middleware.StatsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dydict',
    'loggers',
    'usermanagement',
    'stats',
    'django.contrib.admin',
    'guess_meaning',
)

if DEBUG:
    INSTALLED_APPS += ('south',)

ROOT_URLCONF = 'following_level.urls'

WSGI_APPLICATION = 'following_level.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format': '%(asctime)s:%(levelname)s:%(pathname)s:%(module)s:%(message)s'
    },
    'simple': {
      'format': '%(asctime)s:%(levelname)s:%(message)s'
    },
  },
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    },
    'fileError': {
      'level': 'DEBUG',
      'class': 'logging.handlers.RotatingFileHandler',
      'filename': 'logconfig.log',
      'formatter': 'verbose',
    },
    'mysqlError': {
      'level': 'WARNING',
      'class': 'loggers.handlers.HandlerDB',
      'formatter': 'verbose',
    },
    'custom': {
      '()': 'loggers.handlers.HandlerDB',
      #'alternate': 'cfg://handlers.mail_admins'
    },
  },
  'loggers': {
    'django': {
      'handlers': ['mail_admins', 'mysqlError', 'fileError'],
      'level': 'DEBUG',
      'propagate': True,
    },
    'dydict': {
      'handlers': ['mail_admins', 'mysqlError', 'fileError'],
      'level': 'DEBUG',
      'propagate': True,
    },
    'usermanagement': {
      'handlers': ['mail_admins', 'mysqlError', 'fileError'],
      'level': 'DEBUG',
      'propagate': True,
    },
    'stats': {
      'handlers': ['mail_admins', 'mysqlError', 'fileError'],
      'level': 'DEBUG',
      'propagate': True,
    },
  }
}

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/dictionary/list/'
