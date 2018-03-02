from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import config


_client = MongoClient(
    host=config.MONGO_HOST,
    port=config.MONGO_PORT,
    username=config.MONGO_USERNAME,
    password=config.MONGO_PASSWORD,
    authSource=config.MONGO_AUTH_DB,
)
_database = _client[config.MONGO_DB]

users = _database['users']
users.create_index('google_id', unique=True)
users.create_index('email', unique=True)

sessions = _database['sessions']
sessions.create_index('token', unique=True)


def db():
    try:
        _database.command('ping')
    except ConnectionFailure:
        pass

    return _database
