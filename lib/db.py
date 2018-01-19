import psycopg2

import config
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

def _make_connection():
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        dbname=config.POSTGRES_DBNAME,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )


def db_cursor():
    try:
        # PING
        _conn = _make_connection()
        _conn.cursor.execute('SELECT 1')
    except psycopg2.OperationalError:
        logger.info("Failed to connect database.")


    return _conn.cursor()