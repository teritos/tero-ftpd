"""Tero FTPD Settings."""

import os
import pathlib

HOST = os.getenv('TERO_FTP_HOST', '0.0.0.0')
PORT = os.getenv('TERO_FTP_PORT', 2121)
PASSIVE_PORTS_MIN = os.getenv('PASSIVE_PORTS_MIN')
PASSIVE_PORTS_MAX = os.getenv('PASSIVE_PORTS_MAX')
ROOTDIR = os.getenv('TERO_FTP_FILES_DIR') or str(pathlib.Path.home() / pathlib.Path('.config/tero'))

SECRET_KEY = os.getenv('DJANGO_SECRET') or 'secret'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('TERO_PGSQL_NAME'),
        'USER': os.getenv('TERO_PGSQL_USER'),
        'HOST': os.getenv('TERO_PGSQL_HOST'),
        'PORT': os.getenv('TERO_PGSQL_PORT'),
        'PASSWORD': os.getenv('TERO_PGSQL_PASSWORD'),
    }
}
REDIS_HOST = os.getenv('TERO_REDIS_HOST')
REDIS_PORT = int(os.getenv('TERO_REDIS_PORT'))
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
        "ROUTING": "teroftpd.routing.channel_routing",
    },
}