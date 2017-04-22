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


LOG_FILENAME = '/tmp/pyftpd.log'

# Set up a specific logger with our desired output level
logger = logging.getLogger('ftpd')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

logger.addHandler(handler)


class DjangoChannelsFTPHandler(FTPHandler):
    """Tero FTP Handler."""

    passive_ports = list(range(settings.PASSIVE_PORTS_MIN, settings.PASSIVE_PORTS_MAX))
    masquerade_address = os.getenv('FTPD_MASQUERADE_ADDRESS')

    def __init__(self, conn, server, ioloop=None):
        logger.debug("Initializing FTP Notification handler...")
        super(DjangoChannelsFTPHandler, self).__init__(conn, server, ioloop)

    def on_connect(self):
        """User connected."""
        logger.debug("%s:%s connected", self.remote_ip, self.remote_port)

    def on_disconnect(self):
        """User disconnected."""
        logger.debug("%s:%s disconnected", self.remote_ip, self.remote_port)

    def on_login(self, username):
        """User logs in."""
        logger.debug("%s logged in!", username)

    def on_logout(self, username):
        """User logs out."""
        logger.debug("%s logged out!", username)

    def on_file_received(self, filepath):
        """File received."""
        logger.info("File received %s", filepath)
        self.handle_file_received(filepath)

    def on_incomplete_file_received(self, filepath):
        """Incomplete File received."""
        logger.info("Incomplete file received %s", filepath)
        self.handle_file_received(filepath)

    def handle_file_received(self, filepath):
        """Send a notification."""
        image = ImageHandler(filepath=filepath, username=self.username)

        if image.is_similar():
            return

        with open(filepath, 'rb') as image:
            encoded_image = base64.b64encode(image.read())

        channel_layer.send('mordor.images', {
            'sender': 'ftpd',
            'encoded_image': encoded_image,
            'username': self.username,
            'filetype': PurePosixPath(filepath).suffix,
        })
