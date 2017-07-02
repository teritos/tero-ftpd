import os
import psycopg2


PGSQL_NAME = os.getenv('PGSQL_NAME')
PGSQL_USER = os.getenv('PGSQL_USER')
PGSQL_HOST = os.getenv('PGSQL_HOST')
PGSQL_PORT = os.getenv('PGSQL_PORT', 5432)
PGSQL_SECRET = os.getenv('PGSQL_SECRET')


conn = psycopg2.connect(dbname=PGSQL_NAME,
                        user=PGSQL_NAME,
                        password=PGSQL_SECRET,
                        host=PGSQL_HOST,
                        port=PGSQL_PORT)



class Alarm(object):
    @classmethod
    def is_active_for(cls, username):
        cursor = conn.cursor()
        query = "SELECT alarm_alarm.active FROM alarm_alarm INNER JOIN auth_user ON (alarm_alarm.owner_id = auth_user.id) WHERE auth_user.username = '%s';" % (username,)
        cursor.execute(query)
        try:
            return cursor.fetchone()[0]
        except (IndexError, TypeError):
            return False
