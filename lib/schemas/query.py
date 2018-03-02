from flask import abort
import graphene

from lib.helper import nstr
from lib.mongo import db
from lib.loader.user import filter_user_fields
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
        id=graphene.ID(),
    )
    article_by_id = graphene.Field(
        type=Article,
        id=graphene.ID(),
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

        user = await info.context.loaders.user.load(user_id)
        if user is None:
            abort(401)

        filter_user_fields(user, info.context)
        return user

    async def resolve_user_by_id(self, info, id):
        user = await info.context.loaders.user.load(id)
        filter_user_fields(user, info.context)
        return user

    async def resolve_article_by_id(self, info, id):
        article = await info.context.loaders.article.load(id)
        filter_article_fields(article, info.context)
        return article

    def resolve_article_count(self, info):
        return db().articles.count()

    def resolve_latest_articles(self, info, count, offset):
        articles = []

        results = db().articles.find().skip(offset).limit(count)

        for result in results:
            article = Article(
                id=result['_id'],
                author_id=result['author_id'],
                title=result['title'],
                content=result['content'],
                tags=result.get('tags', []),
                created_at=str(result['created_at']),
                updated_at=str(result['updated_at']),
                published_at=nstr(result.get('published_at')),
            )

            filter_article_fields(article, info.context)
            articles.append(article)

        return articles
