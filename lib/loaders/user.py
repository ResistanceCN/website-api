from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.helper import nstr
from lib.mongo import db
import lib.schemas.types.user


def filter_user_fields(user, context):
    if user is None:
        return

    if isinstance(user, list):
        for i in user:
            filter_user_fields(i, context)
        return

    if context.user.is_admin:
        return

    user.hide_field('google_id')
    user.hide_field('is_admin')

    if user.id != context.user.id:
        user.hide_field('email')


class UserLoader(DataLoader):
    def get_cache_key(self, key):
        return ObjectId(key)

    def batch_load_fn(self, keys):
        keys = [ObjectId(k) for k in keys]

        users = {}
        for result in db().users.find({'_id': {'$in': keys}}):
            users[result['_id']] = lib.schemas.types.user.User(
                id=result['_id'],
                google_id=result['google_id'],
                email=result['email'],
                avatar=nstr(result.get('avatar')),
                is_admin=result['is_admin'],
                name=result['name'],
                faction=result['faction'],
                created_at=str(result['created_at']),
            )

        return Promise.resolve([users.get(key) for key in keys])
