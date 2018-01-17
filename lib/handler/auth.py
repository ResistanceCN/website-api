from flask import request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
import pickle
import uuid

import config
from lib.stdclass import StdClass
from lib.definition import Faction
from lib.db import db_cursor
from lib.redis import redis


def auth():
    token = request.form['google_token']

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), config.GOOGLE_CLIENT_ID)

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        google_id = id_info['sub']

        cur = db_cursor()
        cur.execute('SELECT id, faction, is_admin FROM users WHERE google_id=%s;', (google_id,))
        data = cur.fetchone()

        user_info = StdClass(
            id=data[0],
            faction=Faction(data[1]),
            is_admin=data[2],
        )
        token = str(uuid.uuid4())

        redis.set(token, pickle.dumps(user_info), nx=True)
        # redis.set(token, pickle.dumps(user_info), nx=True, ex=86400)

        return '{"token":"' + token + '"}'
    except Exception:
        abort(401)
