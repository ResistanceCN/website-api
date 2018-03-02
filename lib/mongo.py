from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import config


_client = MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)
_database = _client[config.MONGO_DB]

users = _database['users']
users.create_index('google_id')
users.create_index('email')

sessions = _database['sessions']
sessions.create_index('token')


def db():
    try:
        _database.command('ping')
    except ConnectionFailure:
        pass

    return _database
