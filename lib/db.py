import psycopg2

import config


def _make_connection():
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        dbname=config.POSTGRES_DBNAME,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )


def db_cursor():
    global _conn, _test_cursor

    try:
        # PING
        _test_cursor.execute('SELECT 1')
    except psycopg2.OperationalError:
        # Reconnect
        _conn = _make_connection()
        _test_cursor = _conn.cursor()

    return _conn.cursor()


_conn = _make_connection()
_test_cursor = _conn.cursor()
