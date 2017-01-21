import os
import logging
import redis

from teroftpd.settings import REDIS_HOST
from libtero.images import ImageHash


logger = logging.getLogger("ftpd")

# pylint: disable=invalid-name
r = redis.StrictRedis(host=REDIS_HOST, port=6379)

MOTION_TTL = os.getenv('MOTION_TTL', 60) # seconds
SIMILARITY_THRESHOLD = os.getenv('SIMILARITY_THRESHOLD', 0.8)


class ImageHandler(object):
    """Handle Image."""

    def __init__(self, filepath=None, username=None):
        self.filepath = filepath
        self.username = username

    def is_similar(self):
        image_hash = ImageHash(filepath=self.filepath)
        key = 'motion.{}'.format(self.username)

        # first image
        if not r.exists(key):
            r.set(key, str(image_hash), MOTION_TTL)

        # inside MOTION_TTL
        else:
            last_value = r.get(key).decode('ascii')
            last_hash = ImageHash.from_string(last_value)

            ttl = r.ttl(key)
            r.set(key, str(image_hash), ttl)

            score = image_hash.compare(last_hash)

            logger.info("{} / SIMILARITY_THRESHOLD: {}".format(score, SIMILARITY_THRESHOLD))

            if score > SIMILARITY_THRESHOLD:
                return True

        return False