from flask import abort
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
    me = graphene.Field(User)
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

    async def resolve_me(self, info):
        user_id = info.context.user.id
        if user_id == 0:
            abort(401)

        user = await user_loader.load(user_id)
        filter_user_fields(user, info.context)
        return user

    async def resolve_user_by_id(self, info, id):
        user = await user_loader.load(id)
        filter_user_fields(user, info.context)
        return user

    async def resolve_article_by_id(self, info, id):
        article = await article_loader.load(id)
        filter_article_fields(article, info.context)
        return article

    def resolve_article_count(self):
        cur = db_cursor()
        result = cur['articles'].count({'published_at': {'$exists': True}})
        cur.close()
        return result

    def resolve_latest_articles(self, info, count, offset):
        articles = []
        cur = db_cursor()
        results = cur['articles'].find({'published_at': {'$exists': True}}).sort({'id': -1}).skip(count).limit(offset)
        cur.close()

        for result in results:
            article = Article(
                id=result['id'],
                author_id=result['author_id'],
                title=result['title'],
                content=result['content'],
                tags=result['tags'],
                created_at=str(result['created_at']),
                updated_at=str(result['updated_at']),
                published_at=str(result['published_at']),
            )

            if not isinstance(article.tags, list):
                article.tags = []

            filter_article_fields(article, info.context)
            articles.append(article)

        return articles
