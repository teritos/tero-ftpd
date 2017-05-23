"""Handle ftpd images."""
import os
import redis
import logging  # pylint: disable=C0411

from teroftpd import settings
from libtero.images import ImageHash


logger = logging.getLogger("ftpd")  # pylint: disable=C0103

# pylint: disable=invalid-name
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

MOTION_TTL = os.getenv('MOTION_TTL', 60) # seconds
SIMILARITY_THRESHOLD = os.getenv('SIMILARITY_THRESHOLD', 0.8)


class ImageHandler(object):
    """Handle Image."""

    def __init__(self, filepath=None, username=None):
        self.filepath = filepath
        self.username = username

    def is_similar(self):
        """Return bool if images are similar."""
        image_hash = ImageHash(filepath=self.filepath)
        key = 'motion.{}'.format(self.username)
        ttl = r.ttl(key)

        # key doenst exists
        if ttl == -2:
            r.set(key, str(image_hash), MOTION_TTL)
        # Key returns -1 if key exists but has not associated expire
        elif ttl == -1:
            r.set(key, str(image_hash), MOTION_TTL)
        else:
            last_value = r.get(key).decode('ascii')
            last_hash = ImageHash.from_string(last_value)
            score = image_hash.compare(last_hash)
            logger.info("%s / SIMILARITY_THRESHOLD: %s", score, SIMILARITY_THRESHOLD)

            if score > SIMILARITY_THRESHOLD:
                return True

        return False
