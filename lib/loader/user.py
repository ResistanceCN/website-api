from promise import Promise
from promise.dataloader import DataLoader

from lib.helper import nstr
from lib.mongo import db
import lib.schemas.user


def _get_user(user_id):
    try:
        cur = db_cursor()
        cur.execute('SELECT google_id, email, is_admin, name, faction, created_at '
                    'FROM users WHERE id=%s', (user_id,))
        result = cur.fetchone()
        cur.close()

        user = lib.schemas.user.User(
            id=user_id,
            google_id=result[0],
            email=result[1],
            is_admin=result[2],
            name=result[3],
            faction=result[4],
            created_at=str(result[5]),
        )

        return user
    except Exception:
        return None


def filter_user_fields(user, context):
    if isinstance(user, list):
        for i in user:
            filter_user_fields(i, context)
    else:
        if not context.user.is_admin:
            user.google_id = None
            user.is_admin = None

        if id != context.user.id:
            user.email = None


class UserLoader(DataLoader):
    def batch_load_fn(self, keys):
        users = {}
        for result in db().users.find({'_id': {'$in': keys}}):
            users[result['_id']] = lib.schemas.user.User(
                id=result['_id'],
                google_id=result['google_id'],
                email=result['email'],
                is_admin=result['is_admin'],
                name=result['name'],
                faction=result['faction'],
                created_at=str(result['created_at']),
            )

        return Promise.resolve([users.get(key) for key in keys])
