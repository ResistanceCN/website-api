from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.helper import nstr
from lib.mongo import db
import lib.schemas.user


def filter_user_fields(user, context):
    if user is None:
        return

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
        keys = [ObjectId(k) for k in keys]

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
