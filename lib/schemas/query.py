import json
import graphene

from lib.db import db_cursor
from lib.loader.user import user_loader, filter_user_fields
from lib.loader.article import article_loader, filter_article_fields
from lib.loader.article import filter_article_fields
from .user import User
from .article import Article


class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(default_value="world"),
    )
    user_by_id = graphene.Field(
        type=User,
        id=graphene.Int(),
    )
    article_by_id = graphene.Field(
        type=Article,
        id=graphene.Int(),
    )
    article_count = graphene.Int()
    latest_articles = graphene.Field(
        type=graphene.List(of_type=Article),
        count=graphene.Int(default_value=15),
        offset=graphene.Int(default_value=0),
    )

    def resolve_hello(self, info, name):
        print(info.context)
        return 'Hello ' + name

    async def resolve_user_by_id(self, info, id):
        user = await user_loader.load(id)
        filter_user_fields(user, info.context)
        return user

    async def resolve_article_by_id(self, info, id):
        article = await article_loader.load(id)
        filter_article_fields(article, info.context)
        return article

    def resolve_article_count(self, info):
        cur = db_cursor()
        cur.execute('select count(published_at) from articles')
        result = cur.fetchone()
        cur.close()

        return result[0]

    def resolve_latest_articles(self, info, count, offset):
        articles = []

        cur = db_cursor()
        cur.execute('SELECT id, author_id, title, content, tags, created_at, updated_at, published_at '
                    'FROM articles WHERE published_at IS NOT NULL '
                    'ORDER BY id DESC LIMIT %s OFFSET %s', (count, offset))
        results = cur.fetchall()
        cur.close()

        for result in results:
            article = Article(
                id=result[0],
                author_id=result[1],
                title=result[2],
                content=result[3],
                tags=result[4],
                created_at=str(result[5]),
                updated_at=str(result[6]),
                published_at=str(result[7]),
            )

            if not isinstance(article.tags, list):
                article.tags = []

            filter_article_fields(article, info.context)
            articles.append(article)

        return articles
