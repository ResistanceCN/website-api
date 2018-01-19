from promise import Promise

from .loader import Loader
from lib.db import db_cursor
import lib.schemas.article


def _get_article(article_id):
    try:
        cur = db_cursor()
        cur.execute('SELECT author_id, title, content, tags, created_at, updated_at, published_at '
                    'FROM articles WHERE id=%s', (article_id,))
        result = cur.fetchone()
        cur.close()

        article = lib.schemas.article.Article(
            id=article_id,
            author_id=result[0],
            title=result[1],
            content=result[2],
            tags=result[3],
            created_at=str(result[4]),
            updated_at=str(result[5]),
            published_at=str(result[6]),
        )

        if not isinstance(article.tags, list):
            article.tags = []

        return article
    except Exception:
        return None


def filter_article_fields(article, context):
    if isinstance(article, list):
        for i in article:
            filter_article_fields(i, context)
    else:
        pass


class ArticleLoader(Loader):
    def batch_load_fn(self, keys):
        return Promise.resolve([_get_article(key) for key in keys])


article_loader = ArticleLoader(timeout=300)
