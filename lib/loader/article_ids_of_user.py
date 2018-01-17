from promise import Promise

from .loader import Loader
from lib.db import db_cursor


def _get_article_ids(user_id):
    try:
        cur = db_cursor()
        cur.execute('SELECT id FROM articles WHERE author_id=%s', (user_id,))
        results = cur.fetchall()
        cur.close()

        article_ids = [result[0] for result in results]

        return article_ids
    except Exception:
        return None


class ArticleIdsOfUserLoader(Loader):
    def batch_load_fn(self, keys):
        return Promise.resolve([_get_article_ids(key) for key in keys])


article_ids_of_user_loader = ArticleIdsOfUserLoader()
