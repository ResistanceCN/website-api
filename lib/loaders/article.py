from promise import Promise
from promise.dataloader import DataLoader
from bson.objectid import ObjectId

from lib.helper import nstr
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
            articles[result['_id']] = lib.schemas.types.article.Article(
                id=result['_id'],
                author_id=result['author_id'],
                title=result['title'],
                content=result['content'],
                tags=result.get('tags', []),
                created_at=str(result['created_at']),
                updated_at=str(result['updated_at']),
                published_at=nstr(result.get('published_at')),
            )

        return Promise.resolve([articles.get(key) for key in keys])
