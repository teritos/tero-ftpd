"""Tero FTPD Authorizers."""
import os
import logging
import sqlite3

import bcrypt
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.authorizers import AuthenticationFailed
from db import Alarm

from teroftpd import settings


DEFAULT_PERMISSIONS = "elradfmw"
logger = logging.getLogger()  # pylint: disable=C0103
sqlt = sqlite3.connect(settings.USERS_DB_FILE)
sqlt.execute('''CREATE TABLE  IF NOT EXISTS users
             (username text, password text, homedir text, perms text, active text, msg_login text, msg_quit text)''')


class FTPDjangoUserAuthorizer(DummyAuthorizer):
    """
    FTPD Authorizer that use DJANGO users decorated with FTPUser model
    """

    def __init__(self, rootdir):
        self.rootdir = rootdir

    def add_user(self, username, password, homedir, perm='elr',
                 msg_login="Login successful.", msg_quit="Goodbye."):

        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        sqlt.execute("INSERT INTO users (username, password, homedir, perms, active, msg_login, msg_quit)"
                     "VALUES (?, ?, ?, ?, ?, ?, ?)", [username, bcrypt.hashpw(password, bcrypt.gensalt()), homedir, perm, True, msg_login, msg_quit])
        sqlt.commit()

    def remove_user(self, username):
        """Remove a user from the virtual users table."""
        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        sqlt.execute("DELETE FROM users WHERE username=?", [username])
        sqlt.commit()

    def get_home_dir(self, username):
        """Return the user's home directory.
        Since this is called during authentication (PASS),
        AuthenticationFailed can be freely raised by subclasses in case
        the provided username no longer exists.
        """

        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT homedir FROM users WHERE username=?", [username])
        data = query.fetchone()
        if data is not None:
            return data[0]

    def has_user(self, username):
        """Whether the username exists in the virtual users table."""

        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT count(*) FROM users WHERE username=?", [username])
        data = query.fetchone()
        return bool(data[0])

    def _check_password(self, username, password):
        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT password FROM users WHERE username=?", [username])
        data = query.fetchone()
        return bcrypt.checkpw(password, data[0])

    def get_perms(self, username):
        # No check permissions
        return DEFAULT_PERMISSIONS

    def validate_authentication(self, username, password, handler):
        """Validate user and password."""

        _ = handler
        logger.info("Authenticating user %s...", username)

        # prepare user's homedir and perms
        root_homedir = os.path.join(settings.ROOTDIR, username)
        perm = 'elawdm'

        # Check if alarms is activated
        alarm_active = get_alarm_info_from(username)


        # If alarm is not activated refuse authentication
        if alarm_active is False:
            logger.info('User %s alarm is deactivated, ignoring session', username)
            raise AuthenticationFailed()


        # TODO: Block accounts creations with some lookup table or check if email exists
        # on tero-saas before create account.
        # First time users authenticate create account
        if not self.has_user(username):
            logger.debug('Agregar usuario %s, con password %s y home %s',
                         username, password, root_homedir)
            self.add_user(username, password, root_homedir, perm)

        elif self._check_password(username, password) is True:
            logger.debug('Usuario autenticado %s, con password %s',
                         username, password)
        else:
            raise AuthenticationFailed()

        os.makedirs(root_homedir, exist_ok=True)

    def get_msg_login(self, username):
        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT * FROM users WHERE username=?", [username])
        data = query.fetchone()
        return 'login hola'
        if data is not None:
            return data[0]['msg_login']
        else:
            return ""

    def get_msg_quit(self, username):
        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT * FROM users WHERE username=?", [username])
        data = query.fetchone()
        return 'quit chau'
        if data is not None:
            return data[0]['msg_login']
        else:
            return ""

    def has_perm(self, username, perms, path=None):
        """Should return True if the path is a sub path of home dir."""
        return True
        

def get_alarm_info_from(username):
    """Authenticate a user."""
    return Alarm.is_active_for(username)
