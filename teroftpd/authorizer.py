"""Tero FTPD Authorizers."""
import os
import logging

from teroftpd import settings
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.authorizers import AuthenticationFailed


logger = logging.getLogger("ftpd")  # pylint: disable=C0103


class FTPDjangoUserAuthorizer(DummyAuthorizer):
    """
    FTPD Authorizer that use DJANGO users decorated with FTPUser model
    """

    def __init__(self, rootdir):
        self.root = rootdir
        super(FTPDjangoUserAuthorizer, self).__init__()

    def validate_authentication(self, username, password, handler):
        """Validate user and password."""
        _ = handler
        logger.info("Authenticating user %s...", username)
        alarm_info = get_alarm_info_from(username)
        alarm = alarm_info.get('alarm')
        alarm_status = alarm.get('status')
        if alarm_status != 'active':
            logger.info('User %s alarm is deactivated, ignoring session', username)
            raise AuthenticationFailed()

        root_homedir = os.path.join(settings.ROOTDIR, username)
        perm = 'elawdm'
        os.makedirs(root_homedir, exist_ok=True)
        if not self.has_user(username):
            self.add_user(username, password, root_homedir, perm)


def get_alarm_info_from(username):
    """Authenticate a user."""
    response = {'alarm': {'status': 'active'}}
    return response
