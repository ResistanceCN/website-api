from promise import Promise

from .loader import Loader
from lib.db import db_cursor
import lib.schemas.user


def _get_user(user_id):
    try:
        cur = db_cursor()
        cur.execute('SELECT google_id, email, is_admin, username, faction, created_at '
                    'FROM users WHERE id=%s', (user_id,))
        result = cur.fetchone()
        cur.close()

        user = lib.schemas.user.User(
            id=user_id,
            google_id=result[0],
            email=result[1],
            is_admin=result[2],
            username=result[3],
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


class UserLoader(Loader):
    def batch_load_fn(self, keys):
        return Promise.resolve([_get_user(key) for key in keys])


user_loader = UserLoader(timeout=300)
