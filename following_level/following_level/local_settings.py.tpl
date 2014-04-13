ADMINS = (
  ('', ''),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []

SECRET_KEY = '6@wy+1yh51cih)u_x5i!u9m7@=)+1b#+22irz60nak=c7b=!=8'

STATIC_ROOT = ''

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dydict',
    'djcelery',
    'south',
    'manage_word',
    'loggers',
)

BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Celery
import djcelery
djcelery.setup_loader()
