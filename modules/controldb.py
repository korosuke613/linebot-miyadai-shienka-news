import urllib.request
import psycopg2


class DatabaseControl:
    def __init__(self, db_url_):
        self._database_url = urllib.parse.urlparse(db_url_)
        self.conn = psycopg2.connect(
            database=self._database_url.path[1:],
            user=self._database_url.username,
            password=self._database_url.password,
            host=self._database_url.hostname,
            port=self._database_url.port
        )
        self.cur = self.conn.cursor()

    def close_connect(self):
        self.cur.close()
        self.conn.close()
