"""FTPD Server handlers."""

import os
import base64
import logging
import logging.handlers
from pathlib import PurePosixPath
from pyftpdlib.handlers import FTPHandler
from teroftpd.asgi import channel_layer
from teroftpd.images import ImageHandler
from teroftpd import settings


LOG_FILENAME = '/logs/ftpd.log'
VISION_CONSUMER_KEY = 'vision.images'

# Set up a specific logger with our desired output level
logger = logging.getLogger('ftpd')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

logger.addHandler(handler)
raven = settings.RAVEN_CLIENT


class DjangoChannelsFTPHandler(FTPHandler):
    """Tero FTP Handler."""

    banner = "teroftpd ready."
    max_login_attempts = 1
    passive_ports = list(range(settings.PASSIVE_PORTS_MIN, settings.PASSIVE_PORTS_MAX))
    masquerade_address = os.getenv('FTPD_MASQUERADE_ADDRESS')

    def __init__(self, conn, server, ioloop=None):
        logger.debug("Initializing FTP Notification handler...")
        super(DjangoChannelsFTPHandler, self).__init__(conn, server, ioloop)

    def on_file_received(self, filepath):
        """File received."""
        logger.info("File received %s", filepath)
        try:
            self.handle_file_received(filepath)
        except:
            raven.captureException()

    def on_incomplete_file_received(self, filepath):
        """Incomplete File received."""
        logger.info("Incomplete file received %s", filepath)
        try:
            self.handle_file_received(filepath)
        except:
            raven.captureException()

    def handle_file_received(self, filepath):
        """Send a notification."""
        image = ImageHandler(filepath=filepath, username=self.username)

        # If new image is very different, send image to be processed by mordor
        if not image.is_similar():
            with open(filepath, 'rb') as image:
                encoded_image = base64.b64encode(image.read())
            logger.debug('%s is very different from previous images, sending to process...', filepath)
            channel_layer.send(VISION_CONSUMER_KEY, {
                'sender': 'ftpd',
                'encoded_image': encoded_image,
                'username': self.username,
                'filetype': PurePosixPath(filepath).suffix,
            })

        # Finally, remove image from disk
        os.unlink(filepath)
