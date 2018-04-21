from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.mongo import db
import lib.schemas.types.article


def filter_article_fields(article, context):
    if article is None:
        return

    if isinstance(article, list):
        for i in article:
            filter_article_fields(i, context)
        return


class ArticleLoader(DataLoader):
    def get_cache_key(self, key):
        return ObjectId(key)

    def batch_load_fn(self, keys):
        keys = [ObjectId(k) for k in keys]

        articles = {}
        for result in db().articles.find({'_id': {'$in': keys}}):
            article = lib.schemas.types.article.Article.from_dict(result)
            articles[result['_id']] = article

        return Promise.resolve([articles.get(key) for key in keys])
