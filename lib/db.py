from pymongo import MongoClient
import config
import __main__


def connect():
    """Define client."""
    client = MongoClient(
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    return client


def db_cursor():
    """Get database cursor."""
    try:
        db_cursor = client[config.DB_NAME]
        db_cursor['user'].find_one()
    except ConnectionError:
        __main__.logger.info("Failed to connecting MongoDB. HOST: %s, DB: %s" %
                             (config.DB_HOST + config.DB_PORT, config.DB_NAME))
    return db_cursor


client = connect()
