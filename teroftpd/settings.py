"""Tero FTPD Settings."""

import os
import raven

HOST = os.getenv('TERO_FTP_HOST', '0.0.0.0')
PORT = os.getenv('TERO_FTP_PORT', 2121)
PASSIVE_PORTS_MIN = int(os.getenv('PASSIVE_PORTS_MIN'))
PASSIVE_PORTS_MAX = int(os.getenv('PASSIVE_PORTS_MAX'))
ROOTDIR = os.getenv('TERO_FTP_ROOTDIR') or '/ftp-users'
RAVEN_CLIENT = raven.Client(os.getenv('SENTRY_DNS'))

SECRET_KEY = os.getenv('DJANGO_SECRET') or 'secret'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]
LANGUAGE_CODE = 'es-AR'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGSQL_NAME'),
        'USER': os.getenv('PGSQL_USER'),
        'HOST': os.getenv('PGSQL_HOST'),
        'PORT': os.getenv('PGSQL_PORT'),
        'PASSWORD': os.getenv('PGSQL_SECRET'),
    }
}
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = 6379
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
        "ROUTING": "teroftpd.routing.channel_routing",
    },
}
LOGDIR = '/logs'
os.makedirs(LOGDIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class' : 'logging.handlers.RotatingFileHandler',
            'maxBytes' : 1024*1024*20, # 10MB
            'backupCount': 3,
            'formatter': 'simple',
            'filename': os.path.join(LOGDIR, 'teroftpd.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
        },
        'ftpd': {
            'handlers': ['file'],
            'propagate': True,
        },
    }
}
