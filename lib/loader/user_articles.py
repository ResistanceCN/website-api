from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.helper import nstr
from lib.mongo import db
import lib.schemas.article


class UserArticlesLoader(DataLoader):
    def get_cache_key(self, key):
        return ObjectId(key)

    def batch_load_fn(self, keys):
        keys = [ObjectId(k) for k in keys]

        articles = {}
        for key in keys:
            articles[key] = []

        for result in db().articles.find({'author_id': {'$in': keys}}):
            articles[result['author_id']].append(lib.schemas.article.Article(
                id=result['_id'],
                author_id=result['author_id'],
                title=result['title'],
                content=result['content'],
                tags=result.get('tags', []),
                created_at=str(result['created_at']),
                updated_at=str(result['updated_at']),
                published_at=nstr(result.get('published_at')),
            ))

        return Promise.resolve([articles[key] for key in keys])
