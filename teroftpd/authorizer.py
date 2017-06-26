"""Tero FTPD Authorizers."""
import os
import logging

from teroftpd import settings
from pyftpdlib._compat import unicode
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.authorizers import AuthenticationFailed


logger = logging.getLogger("ftpd")  # pylint: disable=C0103
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
                     "VALUES (?, ?, ?, ?, ?, ?, ?)", [username, password, unicode(homedir), perm, True, msg_login, msg_quit])
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
            return unicode(data[0])
        else:
            return None

    def has_user(self, username):
        """Whether the username exists in the virtual users table."""

        sqlt = sqlite3.connect(settings.USERS_DB_FILE)
        query = sqlt.execute("SELECT count(*) FROM users WHERE username=?", [username])
        data = query.fetchone()
        return bool(data[0])


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
            logger.debug('Agregar usuario %s, con password %s y home %s',
                         username, password, root_homedir)
            self.add_user(username, password, unicode(root_homedir), perm)

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
    response = {'alarm': {'status': 'active'}}
    return response
