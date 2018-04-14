from flask import request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from pymongo.errors import DuplicateKeyError
from uuid import uuid4
from time import time

import config
from lib.mongo import db


def auth():
    try:
        google_token = request.args['google_token']
        id_info = id_token.verify_oauth2_token(google_token, requests.Request(), config.GOOGLE_CLIENT_ID)

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        google_id = id_info['sub']

        user = db().users.find_one({'google_id': google_id})
        if user is None:
            token = insert_token({
                'new_user': True,
                'google_id': google_id,
                'email': id_info['email'],
                'expire': time() + 604800,
            })
            delete_inactive({'google_id': google_id}, 3)

            return '{"token":"' + token + '","newUser":true}'

        token = insert_token({
            'user_id': user['_id'],
            'expire': time() + 604800,
        })
        delete_inactive({'user_id': user['_id']}, 5)

        return '{"token":"' + token + '"}'
    except Exception:
        abort(401)


def insert_token(content):
    for i in range(6):
        token = str(uuid4())
        try:
            db().sessions.insert_one({
                **content,
                'token': token
            })
            return token
        except DuplicateKeyError:
            if i == 5:
                raise ValueError("You've hit the jackpot!")


def delete_inactive(cond, active_count):
    active = db().sessions.find(cond).sort('_id', -1).limit(active_count)
    db().sessions.delete_many({
        **cond,
        '_id': {'$nin': [s['_id'] for s in active]},
    })
