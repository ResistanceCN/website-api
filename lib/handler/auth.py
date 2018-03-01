from flask import request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from pymongo.errors import DuplicateKeyError
from uuid import uuid4
from time import time

import config
from lib.mongo import db


def auth():
    token = request.args['google_token']

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), config.GOOGLE_CLIENT_ID)

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        google_id = id_info['sub']

        user = db().users.find_one({'google_id': google_id})
        if user is None:
            return '{"register":true}'

        for i in range(5):
            token = str(uuid4())
            try:
                db().sessions.insert({
                    'user_id': user['_id'],
                    'token': token,
                    'expire': time() + 604800
                })

                return '{"token":"' + token + '"}'
            except DuplicateKeyError:
                pass

        raise ValueError("You've hit the jackpot!")
    except Exception:
        abort(401)
