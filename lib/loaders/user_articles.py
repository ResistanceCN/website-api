from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.mongo import db
import lib.schemas.types.article


class UserArticlesLoader(DataLoader):
    def get_cache_key(self, key):
        return ObjectId(key)

    def batch_load_fn(self, keys):
        keys = [ObjectId(k) for k in keys]

        articles = {}
        for key in keys:
            articles[key] = []

        for result in db().articles.find({'author_id': {'$in': keys}}).sort('_id', -1):
            article = lib.schemas.types.article.Article.from_dict(result)
            articles[result['author_id']].append(article)

        return Promise.resolve([articles[key] for key in keys])
