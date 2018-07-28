from hashlib import md5
import graphene

from .object import ObjectType
import lib.schemas.types.article
import lib.loaders.article


class User(ObjectType):
    id = graphene.ID()
    google_id = graphene.String()
    email = graphene.String()
    name = graphene.String()
    avatar = graphene.String()
    is_admin = graphene.Boolean()
    faction = graphene.Int()
    created_at = graphene.String()
    articles = graphene.List(lambda: lib.schemas.types.article.Article)

    async def resolve_articles(self, info):
        articles = await info.context.loaders.user_articles.load(self.id)

        me = info.context.user
        if me.id != self.id:
            published = lib.schemas.types.article.ArticleStatus.PUBLISHED
            articles = [article for article in articles if article.status == published]

        lib.loaders.article.filter_article_fields(articles, info.context)
        return articles
