"""Tero FTPD Settings."""

import os
import raven
import pathlib

HOST = os.getenv('TERO_FTP_HOST', '0.0.0.0')
PORT = os.getenv('TERO_FTP_PORT', 2121)
PASSIVE_PORTS_MIN = int(os.getenv('PASSIVE_PORTS_MIN'))
PASSIVE_PORTS_MAX = int(os.getenv('PASSIVE_PORTS_MAX'))
ROOTDIR = os.getenv('TERO_FTP_ROOTDIR') or '/ftp-users'
RAVEN_CLIENT = raven.Client(os.getenv('SENTRY_DNS'))

SECRET_KEY = os.getenv('DJANGO_SECRET') or 'secret'
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
