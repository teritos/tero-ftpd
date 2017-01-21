"""Tero FTPD Settings."""

import os
import pathlib

HOST = os.getenv('TERO_FTP_HOST', '0.0.0.0')
PORT = os.getenv('TERO_FTP_PORT', 2121)
confdir = str(pathlib.Path.home() / pathlib.Path('.config/tero'))
ROOTDIR = os.getenv('TERO_FTP_ROOTDIR', confdir)
SECRET_KEY = 'secret'
REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST', '0.0.0.0')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tero',
        'USER': 'postgres',
        'PASSWORD': 'tero',
        'HOST': POSTGRESQL_HOST,
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
        "ROUTING": "teroftpd.routing.channel_routing",
    },
}
PASSIVE_PORTS_MIN = 30000
PASSIVE_PORTS_MAX = 31000
